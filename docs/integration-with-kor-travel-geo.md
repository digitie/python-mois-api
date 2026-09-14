# `kor-travel-geo`와의 통합

이 문서는 `python-mois-api`(이 저장소)와
[`kor-travel-geo`](https://github.com/digitie/kor-travel-geo)를 함께 사용하는 방법과
설계 원칙을 정리합니다. 의사결정 배경은 [`docs/decisions.md`](decisions.md)의 ADR-002/003/004/009에
있습니다.

> **이름 변경**: 이 저장소의 ADR과 이전 문서는 이 프로젝트를 `python-kraddr-geo`
> (`kraddr.geo` 패키지)로 불렀습니다. 현재 배포명은 `kor-travel-geo`, Python 패키지는
> `kortravelgeo`입니다(GitHub 저장소는 동일 저장소를 가리키도록 리다이렉트됩니다). API도
> `v1`(vworld 호환)에서 자체 provider-neutral `v2`(`CandidateV2`)로 진화했습니다. 아래 내용은
> `kor-travel-geo` v2 기준입니다.

## 라이선스 — `mois`는 절대 import하지 않는다

`kor-travel-geo`는 **GPL-3.0-only**입니다. `python-mois-api`는 MIT이므로, `kor-travel-geo`의
소스를 `mois` 안에서 `import`하면 배포 시 라이선스가 전파됩니다(ADR-009와 동일한 이유,
`python-kraddr-base`뿐 아니라 `kor-travel-geo` 자체도 GPL입니다). 그래서 `mois`는:

- `pyproject.toml`에 `kor-travel-geo`/`kortravelgeo` dependency를 추가하지 않습니다.
- `from kortravelgeo import ...`를 어디에서도 작성하지 않습니다.
- 대신 `AddressGeocoder` Protocol(`GeocodingCandidate` 또는 dict-like `Mapping[str, Any]`만
  받음)만 정의하고, **호출자**가 `kor-travel-geo`를 직접 사용해 이 계약에 맞는 얇은 adapter를
  작성합니다. `kor-travel-geo`를 어떻게 배포·라이선싱할지는 그 adapter를 쓰는 프로젝트(예:
  TripMate, `kor-travel-map`)의 책임이지 `mois`의 책임이 아닙니다.

## 책임 경계

| 항목 | 담당 |
|------|------|
| 행정안전부 인허가 OpenAPI 195종 호출 | `python-mois-api` |
| localdata 파일 다운로드와 CP949/EPSG:5174 변환 | `python-mois-api` |
| SQLite/SpatiaLite 적재(`mois_place_master` 등) | `python-mois-api` |
| 도로명주소 전자지도(PostgreSQL+PostGIS) 적재 | `kor-travel-geo` |
| 정/역 지오코딩(`AsyncAddressClient.geocode`, `.reverse`, v2 `CandidateV2`) | `kor-travel-geo` |
| 사서함/다량배달처 우편번호 보강 | `kor-travel-geo` |
| vworld·juso·epost 호환 응답(`v1`), provider-neutral 후보 목록(`v2`) | `kor-travel-geo` |
| 인허가 행의 주소·좌표가 지오코더와 일치하는지 검증 | `python-mois-api` helper + `kor-travel-geo` 클라이언트를 감싼 adapter |

`mois`는 좌표를 **계산하지 않습니다**. 외부 지오코더 결과와 비교만 합니다. 새로 발견된 갭이 있어도
`kor-travel-geo` 쪽 공개 API를 먼저 안정화하는 것이 ADR-002의 우선순위입니다.

## 환경변수 매핑

| 용도 | `mois` 환경변수 | `kor-travel-geo` 환경변수 |
|------|-----------------|----------------------|
| data.go.kr OpenAPI 서비스키 | `DATA_GO_KR_SERVICE_KEY` | — |
| PostgreSQL DSN | — | `KTG_PG_DSN` |
| vworld 폴백 키 | — | `KTG_VWORLD_API_KEY` |
| juso 검색/좌표 변환 키 | — | `KTG_JUSO_API_KEY`, `KTG_JUSO_COORD_API_KEY` |
| epost 우편번호 다운로드 키 | — | `KTG_EPOST_API_KEY` |

`mois`와 `kor-travel-geo`는 같은 프로세스 안에서 함께 import 해도 충돌하지 않습니다(다만 위
라이선스 절 때문에 `mois` 자신은 import하지 않습니다). 한쪽이 다른 쪽의 환경변수를 읽지 않습니다.

## `AddressGeocoder` 계약과 `kor-travel-geo` v2의 차이

`mois.geocoding.AddressGeocoder` Protocol은 `get_coord(request)` / `nearest_road_address_xy(*, x,
y, max_distance_m)`를 요구하고, 반환값은 `GeocodingCandidate` 또는 `Mapping[str, Any]`만
허용합니다(ADR-009). `kor-travel-geo`의 `AsyncAddressClient`는 이름이 다른 메서드
(`geocode(query=...)`, `reverse(lon, lat, ...)`)를 제공하고, `GeocodeV2Response`/
`ReverseV2Response`(각각 `.candidates: tuple[CandidateV2, ...]`)라는 자체 pydantic 모델을
반환합니다. 즉 **`AsyncAddressClient` 인스턴스를 `validate_address_geocoding_probe`에 그대로
넘길 수 없습니다.** 호출자가 다음처럼 얇은 adapter를 작성해야 합니다.

```python
from __future__ import annotations

from typing import Any

from kortravelgeo import AsyncAddressClient  # kor-travel-geo(GPL-3.0) — mois는 이 줄을 갖지 않음
from kortravelgeo.dto.v2 import CandidateV2

from mois import (
    AddressGeocodingProbe,
    LocalDataFileClient,
    record_to_place_record,
    validate_address_geocoding_probe,
)


def _candidate_v2_to_mapping(candidate: CandidateV2) -> dict[str, Any] | None:
    """kor-travel-geo v2 `CandidateV2`를 mois `AddressGeocoder` 계약(dict)으로 변환합니다."""

    if candidate.point is None:
        return None
    address = candidate.address
    return {
        "x": candidate.point.lon,
        "y": candidate.point.lat,
        "crs": "EPSG:4326",
        "road_address": address.road_address if address else None,
        "lot_address": address.parcel_address if address else None,
        "postal_code": address.postal_code if address else None,
        "legal_dong_code": address.legal_dong_code if address else None,
        "road_name_code": address.road_name_code if address else None,
        "building_management_number": (
            address.building_management_number if address else None
        ),
        "source": candidate.source,
        "distance_m": candidate.distance_m,
        "raw": candidate.model_dump(mode="json"),
    }


class KorTravelGeoAdapter:
    """`kor-travel-geo`의 `AsyncAddressClient`를 mois `AddressGeocoder` 계약에 맞춥니다."""

    def __init__(self, client: AsyncAddressClient) -> None:
        self._client = client

    async def get_coord(self, request: dict[str, Any]) -> list[dict[str, Any]]:
        response = await self._client.geocode(query=request["query"], limit=request.get("limit", 1))
        return [
            mapped
            for candidate in response.candidates
            if (mapped := _candidate_v2_to_mapping(candidate)) is not None
        ]

    async def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> dict[str, Any] | None:
        # x/y는 EPSG:4326 (lon, lat) 순서로 넘겨야 합니다. mois 원본은 EPSG:5174이므로
        # 호출 전에 좌표 변환이 필요합니다(아래 "좌표 순서와 CRS" 절 참고).
        response = await self._client.reverse(lon=x, lat=y, radius_m=int(max_distance_m or 200))
        if not response.candidates:
            return None
        return _candidate_v2_to_mapping(response.candidates[0])


async def verify_hospitals(limit: int = 100) -> None:
    async with (
        LocalDataFileClient() as files,
        AsyncAddressClient() as raw_client,
    ):
        geocoder = KorTravelGeoAdapter(raw_client)
        seen = 0
        async for record in files.iter_hospitals():
            probe = AddressGeocodingProbe.from_place_record(
                # PlaceRecord 변환은 mois.record_to_place_record 사용
                record_to_place_record(record),
                distance_tolerance_m=50.0,
            )
            result = await validate_address_geocoding_probe(
                probe,
                geocoder,
                geocoder_crs="EPSG:4326",
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
```

핵심 규칙:

- **async 클라이언트는 async helper**. `kor-travel-geo`는 async-only이기 때문에
  `validate_address_geocoding_probe`를 사용합니다. 동기 지오코더는 호출 전에 TypeError로 거부합니다(ADR-013).
- **좌표 순서는 모델로 잠금**. `Wgs84Point`는 `(lat, lon)`, `KatecPoint`는 `(x, y)`. float 네 개를
  외부로 흘리지 않습니다(ADR-005). `kor-travel-geo` v2의 `PointV2`는 `(lon, lat)` 순서이므로
  adapter에서 `x=point.lon, y=point.lat`로 명시적으로 매핑합니다.
- **CRS는 명시**. `kor-travel-geo` v2는 기본 EPSG:4326(`PointV2.lon/lat`)을 씁니다(v1 REST API는
  vworld 호환 EPSG:5179 `x_extension.point`). `mois` 원본은 EPSG:5174입니다.
  `validate_address_geocoding_probe(..., geocoder_crs="EPSG:4326")`처럼 실제로 쓰는 API
  버전의 좌표계를 명시합니다.
- **응답에 자체 키 추가 금지**. `GeocodingCandidate`는 `kor-travel-geo` v2의 `CandidateV2`와 1:1로
  대응해야 합니다. `lot_address`는 `CandidateV2.address.parcel_address`(지번주소)에 대응합니다.
  새로운 보강 필드는 `kor-travel-geo`의 `CandidateV2.metadata`/`region`에 먼저 만든 뒤 가져옵니다
  (ADR-002).
- **`AsyncAddressClient`는 DB 클라이언트다**. `kor-travel-geo`의 Python 진입점(`AsyncAddressClient`)은
  PostgreSQL `AsyncEngine`을 직접 물고 동작하도록 만들어졌습니다(내장 REST API 서버가 쓰는 것과
  같은 클래스입니다). 별도 서비스에서 붙일 때는 직접 import(DB 접속 + GPL 전파)하지 말고,
  `kor-travel-geo`가 노출하는 REST API(`/address/geocode`, `/address/reverse`, v2 엔드포인트)를
  HTTP로 호출하는 편이 대부분의 경우 더 적합합니다. 위 adapter 예시는 어느 쪽으로 붙이든 그대로
  씁니다 — `AsyncAddressClient` 대신 HTTP 클라이언트를 넣고 `get_coord`/`nearest_road_address_xy`
  안에서 REST 응답(JSON, 이미 `Mapping[str, Any]`)을 같은 필드 이름으로 매핑하면 됩니다.

## 좌표·주소 보강 파이프라인

`docs/travel-planner-architecture.md`에 정리한 일 1회 야간 배치 파이프라인은 이 통합을 다음 단계로
확장할 수 있습니다.

1. `mois`로 195개 업종의 변경분을 `iter_updated`로 수집.
2. `(service_slug, MNG_NO)` 기준 UPSERT(소프트 삭제 포함).
3. 좌표가 비거나 EPSG:5174 → WGS84 변환 결과가 의심스러우면 `kor-travel-geo`의
   `geocode(road_address)`를 (adapter를 통해) 호출.
4. 결과가 `distance_tolerance_m` 안이면 `mois_place_master.lat/lon`, `legal_dong_code`,
   `road_name_code`, `building_management_number`를 채운다. **원본 EPSG:5174 좌표는 덮어쓰지
   않는다**(ADR-005).
5. 검증 실패 행은 `mois_batch_sync_log`에 격리하고 다음 배치에서 재시도하지 않는다.

## 두 저장소의 문서 정책 동기화

`kor-travel-geo` AGENTS.md의 다음 원칙을 이 저장소도 동일하게 따른다(자세한 내용은 ADR-003):

- 사용자 대상 문서는 한국어로 작성한다(공식 식별자만 원문 유지).
- 외부 API 관련 작업은 단순 전달용 wrapper 지양 원칙을 먼저 문서/코드에 반영한 뒤 진행한다.
- 검증된 다른 라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스/출처를 확인한 뒤 코드 자체를
  들여온다(단, `kor-travel-geo`는 GPL이므로 이 규칙은 `mois`에는 적용하지 않는다 — 위 라이선스 절 참고).
- 기본 테스트는 네트워크를 사용하지 않는다(`mois`는 `DATA_GO_KR_SERVICE_KEY`, `kor-travel-geo`는
  PostgreSQL testcontainers를 분리).
