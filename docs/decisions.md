# ADR — 결정 기록

이 저장소의 구조와 외부 의존을 좌우하는 의사결정을 ADR 형태로 누적합니다. 형식은 `python-kraddr-geo`의
[`decisions.md`](https://github.com/digitie/python-kraddr-geo)와 같습니다. 새로운 결정은 번호를 늘리고
취소된 결정은 `Status: superseded by ADR-NNN`으로 표기만 합니다(본문은 보존).

## ADR-001 — `python-mois-api`는 인허가 데이터 제공에 집중하고, 주소 지오코딩은 위임한다

- 상태: 채택
- 시점: 2026-05-24

행정안전부 지방행정 인허가정보 OpenAPI 195종과 localdata 파일 다운로드 195종을 `mois` 패키지가 책임진다.
주소 정규화, 정/역 지오코딩, 도로명주소 전자지도(SHP) 적재는 별도 라이브러리인
[`python-kraddr-geo`](https://github.com/digitie/python-kraddr-geo)에서 담당하며, `mois`는
그쪽 결과와 자기 좌표를 검증하는 helper(`validate_address_geocoding_probe`,
`validate_address_geocoding_probe_async`)만 제공한다.

이렇게 분리한 이유:

- 인허가 데이터는 일 단위 배치/증분이고, 주소·좌표는 도로명주소 갱신 주기(월·분기)와 외부 API 정책에 묶여 있다.
  두 책임을 한 라이브러리에 섞으면 릴리스 주기와 배포 부담이 합쳐진다.
- `python-kraddr-geo`는 PostgreSQL + PostGIS, async-only API, vworld 호환 응답 같은 자체 아키텍처가 있다
  (kraddr-geo `ADR-001`, `ADR-002`, `ADR-003`). `mois`가 비슷한 기능을 재구현하면 두 곳을 따라가야 한다.
- 사용자(TripMate, `python-krtour-map`)는 두 라이브러리를 함께 쓰면 된다. `mois`는 인허가 행을 주고,
  `kraddr-geo`는 그 주소·좌표를 검증/보강한다.

## ADR-002 — 제공자 단순 wrapper 계층을 만들지 않는다

- 상태: 채택
- 시점: 2026-05-24

`data.go.kr` OpenAPI 호출, localdata 파일 다운로드, 외부 검증 API 호출에 대해 단순 전달용
wrapper/adapter/facade/장기 호환 별칭을 추가하지 않는다. 직접 사용할 수 있는 안정된 공개 클라이언트
(`MoisClient`, `MoisClient.aio()`, `LocalDataFileClient`), 타입 모델(`MoisResponse`, `LocalDataRecord`,
`PlaceRecord`), 열거형(`OpenApiKind`, `ConditionOperator`), 보조 함수만 제공한다.

이유는 `python-kraddr-geo` AGENTS.md §"제공자 API 사용 원칙"과 같다. 단순 wrapper는 시그니처만 한 번
더 갱신해야 하는 비용을 만들고, 사용자가 우리 wrapper의 오타·누락을 추가로 디버깅하게 한다. 다른 검증된
라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스/출처를 확인한 뒤 코드 자체를 들여온다.

## ADR-003 — 동기/비동기 둘 다 1급 시민, 신규 진입점은 둘 다 제공한다

- 상태: 채택
- 시점: 2026-05-24

`MoisClient` / `AsyncMoisClient`, `LocalDataFileClient` / `AsyncLocalDataFileClient`,
`validate_address_geocoding_probe` / `validate_address_geocoding_probe_async`는 항상 짝으로
유지한다. 신규 공개 API는 한쪽만 추가하지 않는다.

`python-kraddr-geo`는 ADR-002로 async-only를 선택했지만, `mois`는 동기 ETL/CLI에서도 호출되기 때문에
sync도 유지한다. 단, `mois`가 `kraddr-geo`를 호출하는 통합 경로는 `kraddr-geo`의 async 계약을 따라야 하므로
검증 helper의 async 버전이 1급이다(ADR-001 참조).

## ADR-004 — 좌표 순서와 CRS는 모델로 잠근다

- 상태: 채택
- 시점: 2026-05-24

float 네 개로 좌표를 전달하지 않는다. 원본 EPSG:5174는 `KatecPoint(x, y)`, WGS84는 `Wgs84Point(lat, lon)`,
두 값과 EPSG:5179 변환은 `StationCoordinates`로 묶는다. 외부 인터페이스를 노출할 때 어느 한쪽 순서로
표준화하지 않는다(KATEC/EPSG:5174는 `(x, y)`, WGS84/EPSG:4326 tuple은 `(lat, lon)`).

이 규칙은 [`docs/repeated-mistakes.md`](repeated-mistakes.md)에 사고 사례와 함께 정리한다.

## ADR-005 — 카탈로그는 손으로 옮기지 않는다

- 상태: 채택
- 시점: 2026-05-24

OpenAPI 195개 × 2(info/history) = 390 URL, localdata 파일 다운로드 195종, 응답변수 매핑표는 모두
공공데이터포털 공지 `NOTICE_0000000004566`의 첨부에서 생성된 `src/mois/catalog.py`를 기준으로 관리한다.
손으로 적은 목록은 `docs/api-list.md`, `docs/incremental-openapi.md`, `docs/response-fields.md` 사이의
정합성을 깨뜨려 왔다(반복 실수). 카탈로그를 갱신할 때는 `tools/generate_docs.py`로 세 문서를 함께
재생성한다.

## ADR-006 — 디버그 웹 UI는 별도 패키지로 분리한다

- 상태: 채택
- 시점: 2026-05-24

DB 브라우저(FastAPI + React) 코드는 `packages/mois-debug-ui/` 아래 별도 PEP 621 패키지
`python-mois-debug-ui`로 둔다. 라이브러리 사용자는 `pip install python-mois-api`만으로 FastAPI, uvicorn,
aiosqlite 등 운영 의존성을 받지 않는다.

`python-kraddr-geo`의 프론트엔드 패키지 `kraddr-geo-ui`(Node.js)와 같은 패턴이다(kraddr-geo `ADR-013`).
디버그 UI는 내부망 전용으로 가정하고, 별도 인증 계층을 두지 않는다.

## ADR-007 — 195개 업종은 마스터-디테일 + JSON 컬럼으로 적재한다

- 상태: 채택
- 시점: 2026-05-24

195개 업종 × 평균 약 60개 필드를 단일 와이드 테이블에 펼치지 않는다. 검색·필터링·공간 인덱싱에 쓰는
공통 필드는 `mois_place_master`로 승격하고, 업종별 특수 필드와 원본 raw 값은
`mois_place_detail.specific_data` / `raw_data`(SQLite JSON)에 저장한다. 승격 기준은
[`docs/json-field-promotion.md`](json-field-promotion.md), 전체 구조는
[`docs/travel-planner-architecture.md`](travel-planner-architecture.md)에 있다.

UPSERT 키는 `(service_slug, MNG_NO)`이고, `MNG_NO`가 비어 있는 행은 `missing-mng-no-<sha256>`로 대체한다
(`docs/repeated-mistakes.md`).
