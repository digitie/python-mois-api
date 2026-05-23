# 작업 지침

## 문서 언어 정책

이 저장소의 모든 Markdown/RST 문서는 한글로 작성한다. 공식 API 필드명, 코드 식별자, 명령어, URL, 제공자 원문처럼 그대로 보존해야 하는 값만 영어를 유지한다. 새 문서나 기존 문서를 수정할 때도 이 규칙을 우선한다.

## 역할

이 저장소(GitHub 이름 `python-mois-api`, Python 패키지 `mois`)는 행정안전부 지방행정 인허가정보 OpenAPI 195개 업종과 localdata 파일 다운로드를 Python에서 다루기 위한 **클라이언트 라이브러리**다. DB 브라우저 웹앱은 별도 `apps/db_browser`에서 운영한다.

## 식별자 (혼동 방지)

| 항목 | 값 |
|------|----|
| GitHub 저장소 이름 | `python-mois-api` |
| Python import | `from mois import ...` |
| 환경변수 prefix | `MOIS_*` |
| SQLite DB 경로 | `MOIS_SQLITE_PATH` |
| Provider 이름 | `python-krmois-api` |

## 개발 환경 정책 (PC, WSL)

PC 개발은 **WSL ext4** 위에서 수행한다. NTFS 마운트에서 직접 `git`/`pip`/`uvicorn`을 실행하지 않는다 — 파일 권한, inotify, 심볼릭 링크, 대량 I/O 성능이 모두 저하된다.

- **코드/가상환경**: ext4 (`~/dev/python-mois-api/`)
- **데이터(`artifacts/`)**: NTFS의 프로젝트 디렉토리 아래에 둔다. 작업 디렉토리에는 심볼릭 링크만 두거나 절대경로로 참조한다.
- **카피 정책**: 작업이 완료되면 ext4 → NTFS의 프로젝트 디렉토리로 카피한다. Git은 ext4 쪽이 source of truth.

작업 전에 반드시 다음을 읽는다:

1. `README.md` — 프로젝트 개요와 빠른 시작
2. `SKILL.md` — DO NOT 룰, 자주 묻는 작업, 도메인 어휘
3. `docs/repeated-mistakes.md` — 반복 실수 방지
4. `docs/decisions.md` — 관련 ADR
5. `CHANGELOG.md` — 현재 릴리스 범위

## 지시 우선순위

1. 사용자 요청
2. 이 `AGENTS.md`
3. `SKILL.md`
4. `docs/decisions.md`, `docs/repeated-mistakes.md`
5. `README.md` 및 나머지 `docs/`
6. 기존 코드와 테스트
7. 최소한의, 되돌릴 수 있는 가정

## 절대 하지 말 것 (DO NOT)

1. **단순 전달용 래퍼 금지** — downstream이 직접 사용할 public client, typed model, enum, helper를 제공한다. 단순 전달용 wrapper, 장기 호환 alias, 임시 facade를 만들지 않는다.
2. **API 목록 손 복사 금지** — `src/mois/catalog.py`와 `tools/generate_docs.py`를 기준으로 관리한다. 목록을 직접 손으로 옮기지 않는다.
3. **좌표 원본 덮어쓰기 금지** — EPSG:5174 원본은 보존하고 WGS84 `(lon, lat)`를 추가한다. 좌표 순서는 KATEC이 `(x, y)`, WGS84가 `(lon, lat)`.
4. **빈 값을 0으로 치환 금지** — 의미 없는 빈 문자열은 `None`이다. 숫자 0으로 바꾸지 않는다.
5. **외부 API 키 평문 커밋 금지** — `MOIS_SERVICE_KEY`는 환경변수로만 전달. `.env`는 `.gitignore`에 포함.
6. **localdata 다운로드 순서 무시 금지** — 안내 페이지 GET → 다운로드 제한 확인 → 실제 다운로드 순서를 지킨다. URL만 바로 호출하면 403.
7. **삭제 응답변수 기본 포함 금지** — 붙임3의 삭제 항목은 기본 목록에서 제외한다.
8. **원본 CSV/ZIP을 문서·fixture 경로에 두기 금지** — `artifacts/` 같은 gitignore 대상 경로에 저장한다.
9. **네트워크 사용 기본 테스트 금지** — 기본 테스트는 네트워크를 사용하지 않는다. live 테스트는 `@pytest.mark.live`로 분리.
10. **전체 flat table 금지** — 195개 업종의 특수 칼럼을 하나의 flat table에 모두 펼치지 않는다. 공통 필드는 마스터, 특수 필드는 JSON.

## 제공자 API 사용 원칙

- 외부 API 관련 작업은 단순 전달용 래퍼/어댑터/게이트웨이 지양 원칙을 먼저 확인하고 문서/코드에 반영한 뒤 진행한다.
- downstream(`python-krtour-map`, TripMate 등)에서 필요한 endpoint, pagination, cursor, exception, raw payload 계약이 부족하면 이 저장소의 public API를 먼저 안정화한다.
- 검증된 다른 라이브러리의 구현이 더 적합하면 wrapper로 감싸지 말고 라이선스와 출처를 확인한 뒤 프로젝트 코드에 직접 반영한다.

## 작업 후 체크리스트

- [ ] `python -m pytest -q` 통과
- [ ] `python -m ruff check .` 통과
- [ ] `python -m mypy src/mois` 통과
- [ ] 의사결정이 있었다면 `docs/decisions.md`에 ADR 추가
- [ ] 사용자 가시 변경이면 `CHANGELOG.md` 갱신
- [ ] OpenAPI 목록 변경은 `src/mois/catalog.py`, `docs/api-list.md`, `docs/response-fields.md` 함께 갱신
- [ ] 파일 로더 변경은 좌표 변환, 날짜/시각 변환, 빈 값 보존 테스트 확인

## 검증

```bash
python -m pytest -q
python -m ruff check .
python -m mypy src/mois
```
