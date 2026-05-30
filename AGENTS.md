# 작업 지침

## 문서 언어 정책

이 저장소의 모든 Markdown/RST 문서와 Python docstring은 한국어로 작성한다. 공식 API 필드명, 코드 식별자,
명령어, URL, 제공자 원문처럼 그대로 보존해야 하는 값만 영어를 유지한다. 새 문서나 기존 문서를 수정할 때도
이 규칙을 우선한다.

## 역할과 경계

이 저장소(GitHub `python-mois-api`, Python `mois`)는 행정안전부 지방행정 인허가정보 OpenAPI 195종과
localdata 파일 다운로드 195종을 다루는 **데이터 제공 라이브러리**다. 주소 정규화·정/역 지오코딩은
[`python-kraddr-geo`](https://github.com/digitie/python-kraddr-geo)가 담당하며, `mois`는
`validate_address_geocoding_probe[_async]`로 양쪽 결과를 비교만 한다(ADR-002,
[`docs/decisions.md`](docs/decisions.md)).

디버그 웹 UI는 별도 패키지 `python-mois-debug-ui`(`packages/mois-debug-ui/`)로 운영한다(ADR-007).
라이브러리 사용자는 FastAPI/uvicorn/aiosqlite를 받지 않는다.

## 식별자 (혼동 방지)

| 항목 | 값 |
|------|----|
| GitHub 저장소 이름 | `python-mois-api` |
| Python import | `from mois import ...` |
| 환경변수 prefix | `MOIS_*` |
| SQLite DB 경로 | `MOIS_SQLITE_PATH` |
| 서비스키 환경변수 | `DATA_GO_KR_SERVICE_KEY` |
| Provider 이름 | `python-krmois-api` |

## 개발 환경 정책 (PC, WSL)

PC 개발은 **WSL ext4** 위에서 수행한다. NTFS 마운트에서 직접 `git`/`pip`/`uvicorn`을 실행하지 않는다
— 파일 권한, inotify, 심볼릭 링크, 대량 I/O 성능이 모두 저하된다.

- **코드/가상환경**: ext4 (`~/dev/python-mois-api/`)
- **데이터(`artifacts/`)**: NTFS의 프로젝트 디렉토리 아래에 둔다. 작업 디렉토리에는 심볼릭 링크만 두거나
  절대경로로 참조한다.
- **카피 정책**: 작업이 완료되면 ext4 → NTFS의 프로젝트 디렉토리로 카피한다. Git은 ext4 쪽이
  source of truth.
- **에이전트별 고정 worktree**: ChatGPT Codex는 `F:\dev\mois-codex`, Claude Code는 `F:\dev\mois-claude`, Google Antigravity 2.0은 `F:\dev\mois-antigravity`를 사용한다. 작업마다 브랜치만 새로 만들고, CodeGraph는 worktree마다 1회 `codegraph init -i` 후 `codegraph sync`로 유지한다(ADR-010).

작업 전에 반드시 다음을 읽는다:

1. `README.md` — 프로젝트 개요와 빠른 시작
2. `SKILL.md` — DO NOT 룰, 자주 묻는 작업, 도메인 어휘
3. `docs/decisions.md` — 관련 ADR
4. `docs/integration-with-kraddr-geo.md` — 외부 지오코더와의 통합 전략
5. `docs/repeated-mistakes.md` — 반복 실수 방지
6. `CHANGELOG.md` — 현재 릴리스 범위

## 지시 우선순위

1. 사용자 요청
2. 이 `AGENTS.md`
3. `SKILL.md`
4. [`docs/decisions.md`](docs/decisions.md)의 ADR
5. [`docs/integration-with-kraddr-geo.md`](docs/integration-with-kraddr-geo.md),
   [`docs/travel-planner-architecture.md`](docs/travel-planner-architecture.md),
   [`docs/db-structure.md`](docs/db-structure.md),
   [`docs/repeated-mistakes.md`](docs/repeated-mistakes.md)
6. `README.md`와 나머지 `docs/`
7. 기존 코드와 테스트
8. 최소한의, 되돌릴 수 있는 가정

## 절대 하지 말 것 (DO NOT)

1. **단순 전달용 래퍼 금지** — downstream이 직접 사용할 public client, typed model, enum, helper를
   제공한다. 단순 전달용 wrapper, 장기 호환 alias, 임시 facade를 만들지 않는다(ADR-003).
2. **지오코딩 재구현 금지** — 주소 정규화·정/역 지오코딩은 `python-kraddr-geo`가 책임진다.
   `mois`는 검증 helper만 제공한다(ADR-002).
3. **sync/async 한쪽만 추가 금지** — 신규 공개 진입점은 `MoisClient`/`AsyncMoisClient`,
   `LocalDataFileClient`/`AsyncLocalDataFileClient`,
   `validate_address_geocoding_probe`/`validate_address_geocoding_probe_async`처럼 짝으로 유지한다
   (ADR-004).
4. **API 목록 손 복사 금지** — `src/mois/catalog.py`와 `tools/generate_docs.py`를 기준으로 관리한다.
   목록을 직접 손으로 옮기지 않는다(ADR-006).
5. **좌표 원본 덮어쓰기 금지** — EPSG:5174 원본은 보존하고 WGS84 `(lat, lon)`을 추가한다. float 네 개를
   외부로 흘리지 말고 `KatecPoint`/`Wgs84Point`/`StationCoordinates`로 잠근다(ADR-005).
6. **빈 값을 0으로 치환 금지** — 의미 없는 빈 문자열은 `None`이다. 숫자 0으로 바꾸지 않는다.
7. **외부 API 키 평문 커밋 금지** — `DATA_GO_KR_SERVICE_KEY`는 환경변수로만 전달. `.env`는
   `.gitignore`에 포함.
8. **localdata 다운로드 순서 무시 금지** — 안내 페이지 GET → 다운로드 제한 확인 → 실제 다운로드 순서를
   지킨다. URL만 바로 호출하면 403.
9. **삭제 응답변수 기본 포함 금지** — 붙임3의 삭제 항목은 기본 목록에서 제외한다.
10. **원본 CSV/ZIP을 문서·fixture 경로에 두기 금지** — `artifacts/` 같은 gitignore 대상 경로에
    저장한다.
11. **네트워크 사용 기본 테스트 금지** — 기본 테스트는 네트워크를 사용하지 않는다. live 테스트는
    `@pytest.mark.live`로 분리.
12. **전체 flat table 금지** — 195개 업종의 특수 칼럼을 하나의 flat table에 모두 펼치지 않는다. 공통
    필드는 마스터, 특수 필드는 JSON(ADR-008).
13. **`python-kraddr-base` 의존 금지** — `pyproject.toml`에 `python-kraddr-base`를 추가하지 않고,
    소스에서 `from kraddr.base import …` / `import kraddr.base`를 작성하지 않는다. `PlaceCoordinate`,
    `Address`, `LatLon`, `JibunAddress`, `RoadNameAddress` 같은 `kraddr.base` 값 객체를 인자/반환
    타입으로 받지 않는다. 외부 라이브러리 결과는 `GeocodingCandidate` 또는 dict으로 변환해 전달한다
    (ADR-009).

## 제공자 API 사용 원칙

- 외부 API 관련 작업은 단순 전달용 래퍼/어댑터/게이트웨이 지양 원칙을 먼저 확인하고 문서/코드에 반영한 뒤
  진행한다(ADR-003).
- downstream(`python-krtour-map`, TripMate 등)에서 필요한 endpoint, pagination, cursor, exception,
  raw payload 계약이 부족하면 이 저장소의 public API를 먼저 안정화한다.
- 검증된 다른 라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스와 출처를 확인한 뒤 프로젝트
  코드에 직접 반영한다.

## 작업 후 체크리스트

- [ ] `python -m pytest -q` 통과
- [ ] `python -m ruff check .` 통과
- [ ] `python -m mypy src/mois` 통과
- [ ] 의사결정이 있었다면 `docs/decisions.md`에 ADR 추가
- [ ] 사용자 가시 변경이면 `CHANGELOG.md` 갱신
- [ ] OpenAPI 목록 변경은 `src/mois/catalog.py`, `docs/api-list.md`, `docs/response-fields.md`,
      `docs/incremental-openapi.md`를 `tools/generate_docs.py`로 함께 갱신
- [ ] 파일 로더 변경은 좌표 변환, 날짜/시각 변환, 빈 값 보존 테스트 함께 확인
- [ ] 지오코딩 검증 helper 변경은 sync/async 짝 양쪽을 함께 변경

## 검증

```bash
python -m pytest -q
python -m ruff check .
python -m mypy src/mois
```
