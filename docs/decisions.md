# 의사결정 기록 (ADR)

이 저장소의 구조와 외부 의존을 좌우하는 의사결정을 ADR 형태로 누적한다. 형식은
[`kor-travel-geo`](https://github.com/digitie/kor-travel-geo)(구 `python-kraddr-geo`)의
`decisions.md`와 같다. 새로운 결정은 번호를 늘리고, 취소된 결정은 `Status: superseded by ADR-NNN`으로
표기만 한다(본문은 보존).

---

## ADR-001: 개발 프로세스 표준화

- **일시**: 2026-05-23
- **결정**: `python-kraddr-geo` 프로젝트의 개발 방식을 도입한다.
- **맥락**: 프로젝트 규모가 커지면서 일관된 개발 프로세스, DO NOT 룰, 작업 후 체크리스트, ADR 기록,
  pre-commit hook이 필요해졌다.
- **결과**:
  - `AGENTS.md`에 지시 우선순위, DO NOT 룰, 작업 후 체크리스트 추가
  - `SKILL.md`에 DO NOT 룰, 도메인 어휘 추가
  - `CONTRIBUTING.md`에 작업 전 필독 목록, ADR 프로세스 추가
  - `.pre-commit-config.yaml`에 ruff, mypy hook 추가
  - `pyproject.toml`에 ruff lint 규칙 확대
  - `.gitignore`에 `.env` 패턴 추가

---

## ADR-002 — `python-mois-api`는 인허가 데이터 제공에 집중하고, 주소 지오코딩은 위임한다

- **일시**: 2026-05-24
- **상태**: 채택 (2026-08-29, `python-kraddr-geo` → `kor-travel-geo` 리네임 반영,
  [`docs/integration-with-kor-travel-geo.md`](integration-with-kor-travel-geo.md) 참고)

행정안전부 지방행정 인허가정보 OpenAPI 195종과 localdata 파일 다운로드 195종을 `mois` 패키지가
책임진다. 주소 정규화, 정/역 지오코딩, 도로명주소 전자지도 적재는 별도 라이브러리인
[`kor-travel-geo`](https://github.com/digitie/kor-travel-geo)(구 `python-kraddr-geo`, Python 패키지
`kortravelgeo`, **GPL-3.0-only**)에서 담당하며, `mois`는 그쪽 결과와 자기 좌표를 검증하는
helper(`validate_address_geocoding_probe`, `validate_address_geocoding_probe_async`)만 제공한다.

이렇게 분리한 이유:

- 인허가 데이터는 일 단위 배치/증분이고, 주소·좌표는 도로명주소 갱신 주기(월·분기)와 외부 API 정책에
  묶여 있다. 두 책임을 한 라이브러리에 섞으면 릴리스 주기와 배포 부담이 합쳐진다.
- `kor-travel-geo`는 PostgreSQL + PostGIS, async-only API, vworld 호환(`v1`)/provider-neutral(`v2`)
  응답 같은 자체 아키텍처가 있다. `mois`가 비슷한 기능을 재구현하면 그쪽을 따라가야 한다.
- `kor-travel-geo`는 GPL-3.0-only이고 `mois`는 MIT이다. `mois`가 직접 import하면 라이선스가
  전파되므로, `mois`는 그 소스를 절대 import하지 않고 dict 계약으로만 결과를 받는다(ADR-009).
- 사용자(TripMate, `kor-travel-map`)는 두 라이브러리를 함께 쓰면 된다. `mois`는 인허가 행을 주고,
  `kor-travel-geo`는 그 주소·좌표를 검증/보강한다.

---

## ADR-003 — 제공자 단순 wrapper 계층을 만들지 않는다

- **일시**: 2026-05-24
- **상태**: 채택

`data.go.kr` OpenAPI 호출, localdata 파일 다운로드, 외부 검증 API 호출에 대해 단순 전달용
wrapper/adapter/facade/장기 호환 별칭을 추가하지 않는다. 직접 사용할 수 있는 안정된 공개 클라이언트
(`MoisClient`, `MoisClient.aio()`, `LocalDataFileClient`), 타입 모델(`MoisResponse`, `LocalDataRecord`,
`PlaceRecord`), 열거형(`OpenApiKind`, `ConditionOperator`), 보조 함수만 제공한다.

이유는 `python-kraddr-geo` AGENTS.md §"제공자 API 사용 원칙"과 같다. 단순 wrapper는 시그니처만 한 번
더 갱신해야 하는 비용을 만들고, 사용자가 우리 wrapper의 오타·누락을 추가로 디버깅하게 한다. 다른 검증된
라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스/출처를 확인한 뒤 코드 자체를 들여온다.

---

## ADR-004 — 동기/비동기 둘 다 1급 시민, 신규 진입점은 둘 다 제공한다

- **일시**: 2026-05-24
- **상태**: 채택

`MoisClient` / `AsyncMoisClient`, `LocalDataFileClient` / `AsyncLocalDataFileClient`,
`validate_address_geocoding_probe` / `validate_address_geocoding_probe_async`는 항상 짝으로
유지한다. 신규 공개 API는 한쪽만 추가하지 않는다.

`kor-travel-geo`는 async-only를 선택했지만, `mois`는 동기 ETL/CLI에서도 호출되기 때문에
sync도 유지한다. 단, `mois`가 `kor-travel-geo`를 호출하는 통합 경로는 `kor-travel-geo`의 async
계약을 따라야 하므로 검증 helper의 async 버전이 1급이다(ADR-002 참조).

---

## ADR-005 — 좌표 순서와 CRS는 모델로 잠근다

- **일시**: 2026-05-24
- **상태**: 채택

float 네 개로 좌표를 전달하지 않는다. 원본 EPSG:5174는 `KatecPoint(x, y)`, WGS84는
`Wgs84Point(lat, lon)`, 두 값과 EPSG:5179 변환은 `StationCoordinates`로 묶는다. 외부 인터페이스를
노출할 때 어느 한쪽 순서로 표준화하지 않는다(KATEC/EPSG:5174는 `(x, y)`, WGS84/EPSG:4326 tuple은
`(lat, lon)`).

이 규칙은 [`docs/repeated-mistakes.md`](repeated-mistakes.md)에 사고 사례와 함께 정리한다.

---

## ADR-006 — 카탈로그는 손으로 옮기지 않는다

- **일시**: 2026-05-24
- **상태**: 채택

OpenAPI 195개 × 2(info/history) = 390 URL, localdata 파일 다운로드 195종, 응답변수 매핑표는 모두
공공데이터포털 공지 `NOTICE_0000000004566`의 첨부에서 생성된 `src/mois/catalog.py`를 기준으로 관리한다.
손으로 적은 목록은 `docs/api-list.md`, `docs/incremental-openapi.md`, `docs/response-fields.md` 사이의
정합성을 깨뜨려 왔다(반복 실수). 카탈로그를 갱신할 때는 `tools/generate_docs.py`로 세 문서를 함께
재생성한다.

---

## ADR-007 — 디버그 웹 UI는 별도 패키지로 분리한다

- **일시**: 2026-05-24
- **상태**: 채택

DB 브라우저(FastAPI + React) 코드는 `packages/mois-debug-ui/` 아래 별도 PEP 621 패키지
`python-mois-debug-ui`로 둔다. 라이브러리 사용자는 `pip install python-mois-api`만으로 FastAPI, uvicorn,
aiosqlite 등 운영 의존성을 받지 않는다.

`kor-travel-geo`의 프론트엔드 패키지 `kor-travel-geo-ui`(Node.js, 내부 운영용)와 같은 패턴이다.
디버그 UI는 내부망 전용으로 가정하고, 별도 인증 계층을 두지 않는다.

---

## ADR-008 — 195개 업종은 마스터-디테일 + JSON 컬럼으로 적재한다

- **일시**: 2026-05-24
- **상태**: 채택

195개 업종 × 평균 약 60개 필드를 단일 와이드 테이블에 펼치지 않는다. 검색·필터링·공간 인덱싱에 쓰는
공통 필드는 `mois_place_master`로 승격하고, 업종별 특수 필드와 원본 raw 값은
`mois_place_detail.specific_data` / `raw_data`(SQLite JSON)에 저장한다. 승격 기준은
[`docs/json-field-promotion.md`](json-field-promotion.md), 전체 구조는
[`docs/travel-planner-architecture.md`](travel-planner-architecture.md)에 있다.

UPSERT 키는 `(service_slug, MNG_NO)`이고, `MNG_NO`가 비어 있는 행은 `missing-mng-no-<sha256>`로 대체한다
(`docs/repeated-mistakes.md`).

---

## ADR-009 — `python-kraddr-base`에 의존하지 않는다

- **일시**: 2026-05-27
- **상태**: 채택

`python-mois-api`는 `python-kraddr-base`(`kraddr.base` 패키지)에 직접 의존하지 않는다.
즉, `pyproject.toml`에 dependency를 추가하지 않고, 소스 코드 어디에서도 `from kraddr.base import …`
또는 `import kraddr.base`를 작성하지 않는다. `PlaceCoordinate`, `Address`, `LatLon`, `JibunAddress`,
`RoadNameAddress` 같은 `kraddr.base` 값 객체를 인자/반환 타입으로 받지 않는다.

이유:

- `python-kraddr-base`는 GPL-3.0-or-later 라이선스다. `python-mois-api`는 MIT이므로 의존을 추가하면
  배포 시 라이선스 제약이 함께 따라온다. wrapper 금지 원칙(ADR-003)과도 충돌한다.
- `mois`가 노출해야 하는 값 객체는 카탈로그·인허가 도메인에 특화된 것뿐이다(`KatecPoint`,
  `Wgs84Point`, `StationCoordinates`, `Coordinate`, `LocalDataRecord`, `PlaceRecord`,
  `AddressGeocodingProbe`, `GeocodingCandidate`). 외부 도메인 모델을 재노출하면 두 곳에서 갱신해야
  하는 비용이 생긴다.
- `kor-travel-geo`(구 `python-kraddr-geo`, ADR-002)와 통합할 때는 dict 또는 `GeocodingCandidate`로
  변환된 결과를 받는다. 자세한 인터페이스는 `docs/integration-with-kor-travel-geo.md`에 있다.

이 결정이 코드에 반영되는 방식:

- `AddressGeocoder` Protocol은 후보 타입을 `GeocodingCandidate | Mapping[str, Any]`로 좁힌다.
  임의 객체에 대해 `getattr(obj, "x")` 등을 시도하는 duck typing 경로(`_public_attrs`)는 제거됐다.
- `_candidate_from_any`는 `GeocodingCandidate` 또는 `Mapping`이 아닌 입력에 대해 `TypeError`를 던진다.
- `tests/test_no_kraddr_base.py`가 `src/mois/` 전체에 `kraddr.base` 임포트가 없는지 회귀 방지로
  검증한다.

---

## ADR-010 — 카탈로그 기반 Streamlit 디버그 UI를 `examples/`에 예제 스크립트로 둔다

- **일시**: 2026-08-29
- **상태**: 채택

195개 업종 OpenAPI를 하나씩 골라 호출/응답/가공 결과를 확인하는 가벼운 Streamlit 스크립트를
`examples/streamlit_debug_ui.py`로 추가한다. `python-khoa-api`의 `examples/streamlit_debug_ui.py` +
`src/khoa/debug.py`를 원형으로 다른 자매 저장소들과 함께 수렴 중인 표준 템플릿을 따른다.

- `pyproject.toml`의 `[project.optional-dependencies]`에 `debug-ui = ["pandas>=2", "streamlit>=1.36"]`만
  추가한다. `pip install python-mois-api`만 하는 라이브러리 사용자는 영향을 받지 않는다(ADR-007과
  같은 동기).
- `packages/mois-debug-ui/`(FastAPI + React SQLite DB 브라우저, ADR-007)와는 완전히 다른 도구다.
  이 Streamlit 스크립트는 SQLite를 보지 않고, `MoisClient.debug_request()`로 OpenAPI 195종을 직접
  호출·검증하는 용도다. 서로 대체 관계가 아니므로 `packages/mois-debug-ui/`는 그대로 둔다.
- 파라미터 입력 폼은 `if function_name == ...` 같은 업종별 분기 없이 `get_api_catalog()`가 제공하는
  `required_params`/`optional_params` 메타데이터로만 위젯을 만든다. 195개 업종은 동일한 요청
  파라미터 계약(`serviceKey`/`pageNo`/`numOfRows`/`opnSfTeamCode`/`cond[FIELD::OP]`)을 공유하므로
  `OpenApiService.required_params`/`optional_params` 기본값은 모든 업종에서 동일하다.
- `jsonable`/`redact_sensitive`/`error_to_dict`/`save_fixture`는 모두 `src/mois/debug.py`,
  `src/mois/fixtures.py`에 있는 기존 helper를 그대로 재사용한다(Streamlit 파일에 인라인 재구현하지
  않는다).

---

## ADR-011 — `src/mois/rustfs.py`는 RustFS 미러 업로드를 위한 자체 SigV4 클라이언트다

- **일시**: 2026-08-29
- **상태**: 채택

`src/mois/rustfs.py`는 [RustFS](https://rustfs.com)(Rust로 구현된 S3 호환 오브젝트 스토리지 서버,
자체 호스팅용)에 파일을 업로드하기 위한 동기/비동기 클라이언트(`RustfsClient`/`AsyncRustfsClient`)와
설정(`EffectiveRustfsConfig`)을 제공한다. `LocalDataFileClient`/`AsyncLocalDataFileClient`의
`download_to_rustfs()`와 동적 편의 메서드 `download_<slug>_to_rustfs()`가 이를 사용해, localdata 파일을
로컬에 다운로드하는 동시에 같은 파일을 RustFS 버킷에도 미러링한다. 커밋 `029d14c`(2026-06-07)에서
추가됐으나 README/AGENTS.md/decisions.md 어디에도 설명이 없었다.

- **왜 필요한가**: `tools/load_all_localdata_to_sqlite.py` 같은 배치 적재 파이프라인이나 다운스트림
  ETL(TripMate, `kor-travel-map`)이 다운로드한 원본 CSV를 재현 가능하도록 오브젝트 스토리지에
  보관하려는 용도다. `MOIS_RUSTFS_ENABLED=true`와 `MOIS_RUSTFS_ACCESS_KEY`/`MOIS_RUSTFS_SECRET_KEY`가
  설정된 경우에만 동작하는 완전한 opt-in 기능이며, 기본값(`false`)에서는 기존 `download()` 동작에
  영향을 주지 않는다.
- **왜 `boto3`/`aioboto3`를 쓰지 않았는가**: `pyproject.toml` 의존성은 `httpx`/`pydantic`/`pyproj`/
  `SQLAlchemy`뿐이다. 이 모듈이 실제로 쓰는 S3 오퍼레이션은 버킷 존재 확인(HEAD)과 객체 업로드(PUT)
  둘뿐이라, AWS SDK 전체를 새 의존성으로 들이는 대신 이미 쓰고 있는 `httpx`로 AWS Signature Version
  4 서명을 직접 구현했다(`_signed_request_helper`). 동기/비동기 두 클라이언트를 모두 제공하는 것은
  ADR-004의 sync/async 짝 유지 규칙을 따른 것이다.
- **공개 API 여부**: `RustfsClient`/`AsyncRustfsClient`/`EffectiveRustfsConfig`는 `mois.__init__`의
  `__all__`에 포함된 공개 표면이고 `tests/test_rustfs.py`로 검증된다. 오브젝트 키는 `rustfs://<bucket>/
  <key>` 형태 URI 문자열로 반환한다.

---

## ADR-012 — 메인 패키지 `mois`에는 CLI 진입점(`project.scripts`)을 두지 않는다

- **일시**: 2026-08-29
- **상태**: 채택

`packages/mois-debug-ui/pyproject.toml`에는 `mois-debug-ui`, `mois-debug-ui-load-sqlite` 두
`[project.scripts]` 진입점이 있지만, 루트 `pyproject.toml`(패키지 `mois`)에는 하나도 없다. 이 비대칭은
결함이 아니라 두 패키지의 성격 차이를 그대로 반영한 것이므로 CLI를 추가하지 않는다.

- `mois`는 AGENTS.md 목표에 정의된 대로 downstream이 import해서 쓰는 **데이터 제공 라이브러리**다.
  `pip install python-mois-api`로 설치하는 사용자에게 실행 가능한 커맨드를 제공할 이유가 없다.
- `mois-debug-ui`는 FastAPI + React로 만든 독립 실행형 웹 애플리케이션(ADR-007)이다. 프로세스로 띄워야
  하는 서버이므로 그 자체 CLI 진입점이 자연스럽다. 즉 CLI가 있는 쪽이 예외가 아니라 애플리케이션이라는
  성격의 결과다.
- 저장소 안에서 데이터를 적재/생성하는 운영 스크립트(`tools/load_all_localdata_to_sqlite.py`,
  `tools/generate_docs.py`, `tools/probe_life_convenience.py`)는 이미 `argparse` 기반으로 존재하고
  `python tools/<script>.py`로 직접 실행한다. 이들은 이 저장소 자체의 유지보수/배치 작업이지 downstream
  라이브러리 사용자에게 배포할 명령이 아니므로, `python -m mois.cli` 같은 새 진입점으로 감쌀 필요가
  없다. 실사용 근거 없이 새 CLI 표면을 추가하는 것은 SKILL.md §4의 "단순 전달용 래퍼 금지" 원칙과도
  맞지 않는다.
- 코드 변경은 없다. 이 ADR은 비대칭이 의도된 것임을 기록하는 용도다.
