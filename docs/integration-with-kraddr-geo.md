# `python-kraddr-geo`와의 통합

이 문서는 `python-mois-api`(이 저장소)와
[`python-kraddr-geo`](https://github.com/digitie/python-kraddr-geo)를 함께 사용하는 방법과
설계 원칙을 정리합니다. 의사결정 배경은 [`docs/decisions.md`](decisions.md)의 ADR-002/003/004에 있습니다.

## 책임 경계

| 항목 | 담당 |
|------|------|
| 행정안전부 인허가 OpenAPI 195종 호출 | `python-mois-api` |
| localdata 파일 다운로드와 CP949/EPSG:5174 변환 | `python-mois-api` |
| SQLite/SpatiaLite 적재(`mois_place_master` 등) | `python-mois-api` |
| 도로명주소 전자지도(SHP) 적재 | `python-kraddr-geo` |
| 정/역 지오코딩(`AsyncAddressClient.geocode`, `reverse_geocode`) | `python-kraddr-geo` |
| 사서함/다량배달처 우편번호 보강 | `python-kraddr-geo` |
| vworld·juso·epost·Kakao Maps 호환 응답(`x_extension`) | `python-kraddr-geo` |
| 인허가 행의 주소·좌표가 지오코더와 일치하는지 검증 | `python-mois-api` helper + `kraddr-geo` 클라이언트 |

`mois`는 좌표를 **계산하지 않습니다**. 외부 지오코더 결과와 비교만 합니다. 새로 발견된 갭이 있어도
`kraddr-geo` 쪽 공개 API를 먼저 안정화하는 것이 ADR-002의 우선순위입니다.

## 환경변수 매핑

| 용도 | `mois` 환경변수 | `kraddr-geo` 환경변수 |
|------|-----------------|----------------------|
| data.go.kr OpenAPI 서비스키 | `DATA_GO_KR_SERVICE_KEY` | — |
| PostgreSQL DSN | — | `KRADDR_GEO_PG_DSN` |
| vworld 폴백 키 | — | `KRADDR_GEO_VWORLD_API_KEY` |
| juso 검색/좌표 변환 키 | — | `KRADDR_GEO_JUSO_API_KEY`, `KRADDR_GEO_JUSO_COORD_API_KEY` |
| epost 우편번호 다운로드 키 | — | `KRADDR_GEO_EPOST_API_KEY` |

`mois`와 `kraddr-geo`는 같은 프로세스 안에서 함께 import 해도 충돌하지 않습니다. 한쪽이 다른 쪽의 환경변수를
읽지 않습니다.

## 검증 워크플로

`mois`의 `PlaceRecord` 한 행을 `kraddr-geo`의 `AsyncAddressClient`로 검증합니다.

```python
import asyncio

from kraddr.geo import AsyncAddressClient
from mois import (
    AddressGeocodingProbe,
    LocalDataFileClient,
    validate_address_geocoding_probe_async,
)


async def verify_hospitals(limit: int = 100) -> None:
    async with (
        LocalDataFileClient.aio() as files,
        AsyncAddressClient() as geocoder,
    ):
        seen = 0
        async for record in files.iter_hospitals():
            probe = AddressGeocodingProbe.from_place_record(
                # PlaceRecord 변환은 mois.record_to_place_record 사용
                record_to_place_record(record),
                distance_tolerance_m=50.0,
            )
            result = await validate_address_geocoding_probe_async(
                probe,
                geocoder,
                geocoder_crs="EPSG:5179",
            )
            if not result.within_tolerance:
                print(
                    f"불일치 {record.management_number}:"
                    f" geocode={result.geocode_distance_m}m"
                    f" reverse={result.reverse_distance_m}m"
                )
            seen += 1
            if seen >= limit:
                return


asyncio.run(verify_hospitals())
```

핵심 규칙:

- **async 클라이언트는 async helper**. `kraddr-geo`는 자기 ADR-002에서 async-only를 못박았기 때문에
  `validate_address_geocoding_probe_async`를 사용합니다. 동기 helper에 코루틴 결과가 들어오면
  `TypeError`로 즉시 거부합니다(ADR-004).
- **좌표 순서는 모델로 잠금**. `Wgs84Point`는 `(lat, lon)`, `KatecPoint`는 `(x, y)`. float 네 개를
  외부로 흘리지 않습니다(ADR-005).
- **CRS는 명시**. `kraddr-geo`는 vworld 호환 응답이라 기본 EPSG:5179(`x_extension.point`)를 씁니다.
  `mois` 원본은 EPSG:5174입니다. `validate_address_geocoding_probe_async(..., geocoder_crs="EPSG:5179")`처럼
  공급자 좌표계를 명시합니다.
- **응답에 자체 키 추가 금지**. `GeocodingCandidate`는 `kraddr-geo`의 `x_extension` 필드와 1:1 매핑되어야
  합니다. 새로운 보강 필드는 `kraddr-geo` `x_extension`에 먼저 만든 뒤 가져옵니다(ADR-002).

## 좌표·주소 보강 파이프라인

`docs/travel-planner-architecture.md`에 정리한 일 1회 야간 배치 파이프라인은 이 통합을 다음 단계로
확장할 수 있습니다.

1. `mois`로 195개 업종의 변경분을 `iter_updated`로 수집.
2. `(service_slug, MNG_NO)` 기준 UPSERT(소프트 삭제 포함).
3. 좌표가 비거나 EPSG:5174 → WGS84 변환 결과가 의심스러우면 `kraddr-geo`의 `geocode(road_address)`를 호출.
4. 결과가 `distance_tolerance_m` 안이면 `mois_place_master.lat/lon`, `legal_dong_code`, `road_name_code`,
   `building_management_number`를 채운다. **원본 EPSG:5174 좌표는 덮어쓰지 않는다**(ADR-005).
5. 검증 실패 행은 `mois_batch_sync_log`에 격리하고 다음 배치에서 재시도하지 않는다.

## 두 저장소의 문서 정책 동기화

`python-kraddr-geo` AGENTS.md의 다음 원칙을 이 저장소도 동일하게 따른다(자세한 내용은 ADR-003):

- 사용자 대상 문서는 한국어로 작성한다(공식 식별자만 원문 유지).
- 외부 API 관련 작업은 단순 전달용 wrapper 지양 원칙을 먼저 문서/코드에 반영한 뒤 진행한다.
- 검증된 다른 라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스/출처를 확인한 뒤 코드 자체를
  들여온다.
- 기본 테스트는 네트워크를 사용하지 않는다(`mois`는 `DATA_GO_KR_SERVICE_KEY`, `kraddr-geo`는 PostgreSQL
  testcontainers를 분리).
