# 작업 지침

이 저장소는 행정안전부 지방행정 인허가정보 OpenAPI와 localdata 파일 다운로드를 다룹니다.

## 역할과 경계

이 저장소(GitHub `python-mois-api`, Python `mois`)는 행정안전부 지방행정 인허가정보 OpenAPI 195종과
localdata 파일 다운로드 195종을 다루는 **데이터 제공 라이브러리**다. 주소 정규화·정/역 지오코딩은
[`python-kraddr-geo`](https://github.com/digitie/python-kraddr-geo)가 담당하며, `mois`는
`validate_address_geocoding_probe[_async]`로 양쪽 결과를 비교만 한다(ADR-001, [`docs/decisions.md`](docs/decisions.md)).

디버그 웹 UI는 별도 패키지 `python-mois-debug-ui`(`packages/mois-debug-ui/`)로 운영한다(ADR-006).
라이브러리 사용자는 FastAPI/uvicorn/aiosqlite를 받지 않는다.

## 기본 원칙

- 사용자 대상 문서와 Python docstring은 한국어로 작성한다. 패키지명, 함수명, 환경변수, URL, 표준 기술명처럼
  코드나 공식 명칭으로 식별해야 하는 값만 원문 표기를 유지한다.
- API/파일/응답변수 목록은 손으로 복사하지 않고 공식 자료에서 생성된 카탈로그(`src/mois/catalog.py`)를
  기준으로 한다(ADR-005).
- 외부 API 관련 작업은 단순 전달용 wrapper/adapter/facade/장기 호환 별칭을 만들지 않는다는 원칙을
  먼저 문서/코드에 반영한 뒤 진행한다(ADR-002).
- 하위 프로젝트(TripMate, `python-krtour-map`)가 직접 사용할 안정된 공개 클라이언트, 타입 모델, 열거형,
  헬퍼를 제공한다. 부족하면 wrapper를 새로 만들지 말고 이 저장소의 공개 API를 먼저 안정화한다.
- 검증된 다른 라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스와 출처를 확인한 뒤 코드 자체를
  들여온다.
- 신규 공개 API는 sync/async 둘 다 제공한다(ADR-003). `MoisClient`/`AsyncMoisClient`,
  `LocalDataFileClient`/`AsyncLocalDataFileClient`,
  `validate_address_geocoding_probe`/`validate_address_geocoding_probe_async`는 항상 짝으로 유지한다.
- 좌표는 float 네 개로 흘리지 말고 `KatecPoint`/`Wgs84Point`/`StationCoordinates`로 잠근다(ADR-004).
- 기본 테스트는 네트워크를 사용하지 않는다. 실제 호출 테스트는 `DATA_GO_KR_SERVICE_KEY`가 있을 때만
  실행되도록 `@pytest.mark.live`로 분리한다.
- 인허가정보 CSV는 CP949, 좌표계는 EPSG:5174라는 전제를 잊지 않는다.

## 변경 전 확인

1. [`docs/decisions.md`](docs/decisions.md) — 관련 ADR이 있는지 확인한다. 결정이 바뀌면 ADR을 추가하고
   기존 ADR은 `Status: superseded by ADR-NNN`만 표기한다(본문 보존).
2. [`docs/repeated-mistakes.md`](docs/repeated-mistakes.md) — 같은 실수를 반복하지 않는다.
3. OpenAPI 목록 변경은 `src/mois/catalog.py`, `docs/api-list.md`, `docs/response-fields.md`,
   `docs/incremental-openapi.md`를 `tools/generate_docs.py`로 함께 갱신한다(ADR-005).
4. 파일 로더 변경은 좌표 변환, 날짜/시각 변환, 빈 값 보존 테스트를 함께 확인한다.
5. 지오코딩 검증 helper 변경은 동기/비동기 짝 양쪽을 함께 변경한다(ADR-003).

## 지시 우선순위

1. 사용자 요청
2. 이 `AGENTS.md`
3. [`docs/decisions.md`](docs/decisions.md)의 ADR
4. [`docs/integration-with-kraddr-geo.md`](docs/integration-with-kraddr-geo.md),
   [`docs/travel-planner-architecture.md`](docs/travel-planner-architecture.md),
   [`docs/db-structure.md`](docs/db-structure.md), [`docs/repeated-mistakes.md`](docs/repeated-mistakes.md)
5. README와 나머지 `docs/`
6. 기존 코드와 테스트
7. 최소한의, 되돌릴 수 있는 가정

## 검증

```bash
python -m pytest
python -m ruff check .
python -m mypy src/mois
```
