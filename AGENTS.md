# 작업 지침

## 목표

`python-mois-api`(GitHub 저장소 이름, Python import `mois`)는 행정안전부 지방행정 인허가정보 OpenAPI
195종과 `file.localdata.go.kr` 파일 다운로드 195종을 하나의 동기/비동기 클라이언트 인터페이스로 감싸는
**데이터 제공 라이브러리**다. 주소 정규화·정/역 지오코딩은 담당하지 않고 별도 라이브러리
[`kor-travel-geo`](https://github.com/digitie/kor-travel-geo)(구 `python-kraddr-geo`, GPL-3.0-only)에
위임하며, `mois`는 그 소스를 import하지 않고 검증 helper(`validate_address_geocoding_probe[_async]`,
ADR-002)로만 연결한다. 디버그 웹 UI는 별도 패키지 `python-mois-debug-ui`(`packages/mois-debug-ui/`)로
분리되어 있다(ADR-007).

## Think Before Coding

- 요청이 모호할 때는 해석을 조용히 정하지 말 것
- 중요한 가정은 숨기지 말고 드러낼 것
- 해석에 따라 구현 방향이 크게 달라지면 그 차이를 먼저 표면화할 것
- 안전하게 진행하기 어려울 정도로 혼란스러우면 추측하지 말고 확인할 것

## Simplicity First

- 요청을 완전히 해결하는 최소한의 코드만 작성할 것
- 요청되지 않은 기능을 추가하지 말 것
- 일회성 용도를 위해 추상화를 만들지 말 것
- 구체적인 필요 없이 설정 가능성이나 유연성을 늘리지 말 것
- 구현이 문제에 비해 커졌다고 느껴지면 줄일 것

## Surgical Changes

- 요청을 처리하는 데 필요한 코드만 변경할 것
- 작업이 요구하지 않으면 주변 로직까지 다시 쓰지 말 것
- 관련 없는 코드의 포맷, 이름, 스타일을 건드리지 말 것
- 사용자가 더 넓은 변경을 원한 것이 아니라면 기존 패턴을 맞출 것
- 관련 없는 문제를 발견하면 패치에 섞지 말고 따로 언급할 것

## Goal-Driven Execution

- 모호한 요청을 구체적이고 검증 가능한 결과로 바꿀 것
- 버그 수정은 재현 없이 바로 신뢰하지 말 것
- 리팩터링은 동작 보존을 전제로 전후 기대를 확인할 것
- 넓고 막연한 점검보다 목적이 분명한 검증을 선호할 것
- 완전한 검증이 불가능하면 무엇이 아직 미검증인지 밝힐 것

## Practical Bias

- 비단순 작업에서는 성급함보다 신중함을 우선할 것
- 변경 내역은 리뷰 가능한 범위와 요청 범위에 가깝게 유지할 것
- 아주 단순하고 명백한 한 줄 작업은 과하게 무겁게 다루지 말 것

## 문서 언어 정책

이 저장소의 모든 Markdown/RST 문서와 Python docstring은 한국어로 작성한다. 공식 API 필드명, 코드 식별자,
명령어, URL, 제공자 원문처럼 그대로 보존해야 하는 값만 영어를 유지한다. 새 문서나 기존 문서를 수정할 때도
이 규칙을 우선한다.

## 식별자 (혼동 방지)

| 항목 | 값 |
|------|----|
| GitHub 저장소 이름 | `python-mois-api` |
| Python import | `from mois import ...` |
| 환경변수 prefix | `MOIS_*` |
| SQLite DB 경로 | `MOIS_SQLITE_PATH` |
| 서비스키 환경변수 | `DATA_GO_KR_SERVICE_KEY` |
| Provider 이름 (`PROVIDER_NAME`) | `python-mois-api` |

## 절대 하지 말 것 (DO NOT)

1. **단순 전달용 래퍼 금지** — downstream이 직접 사용할 public client, typed model, enum, helper를
   제공한다. 단순 전달용 wrapper, 장기 호환 alias, 임시 facade, 게이트웨이는 만들지 않는다(ADR-003).
2. **지오코딩 재구현 금지** — 주소 정규화·정/역 지오코딩은 `kor-travel-geo`(구 `python-kraddr-geo`)가
   책임진다. `mois`는 검증 helper만 제공하고 그 소스를 import하지 않는다(ADR-002, GPL-3.0).
3. **sync/async 한쪽만 추가 금지** — 신규 공개 진입점은 `MoisClient`/`AsyncMoisClient`,
   `LocalDataFileClient`/`AsyncLocalDataFileClient`,
   `validate_address_geocoding_probe`/`validate_address_geocoding_probe_async`처럼 짝으로 유지한다
   (ADR-004).
4. **`python-kraddr-base` 의존 금지** — `pyproject.toml`에 `python-kraddr-base`를 추가하지 않고,
   소스에서 `from kraddr.base import …` / `import kraddr.base`를 작성하지 않는다. 외부 라이브러리 결과는
   `GeocodingCandidate` 또는 dict으로 변환해 전달한다(ADR-009).
5. **API 목록 손 복사 금지** — `src/mois/catalog.py`와 `tools/generate_docs.py`를 기준으로 관리한다.
   목록을 직접 손으로 옮기지 않는다(ADR-006).

세부 데이터 처리 규칙(좌표 보존, 빈 값 처리, localdata 다운로드 순서, flat table 금지 등)은
`SKILL.md` §4에 있다.

## 작업 전 필독

1. `README.md` — 프로젝트 개요와 빠른 시작
2. `SKILL.md` — DO NOT 룰, 자주 묻는 작업, 도메인 어휘
3. `docs/decisions.md` — 관련 ADR
4. `docs/integration-with-kor-travel-geo.md` — 외부 지오코더와의 통합 전략
5. `docs/repeated-mistakes.md` — 반복 실수 방지
6. `CHANGELOG.md` — 현재 릴리스 범위

## 지시 우선순위

사용자 요청 > `AGENTS.md` > `README.md`/`docs/`와 기존 코드·테스트.

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
