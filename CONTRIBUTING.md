# 기여 안내

`python-mois-api`에 기여할 때는 공식 자료와 실제 응답 사이의 차이를 분리해서 기록해 주세요.

## 작업 전 필독

1. `SKILL.md` — DO NOT 룰, 도메인 어휘, 자주 묻는 작업 (필수)
2. `docs/repeated-mistakes.md` — 반복 실수 방지
3. `docs/decisions.md` — 기존 의사결정 기록 (ADR)

## 개발 환경

```bash
pip install -e ".[dev]"
python -m pytest
```

PC 개발은 WSL ext4 위에서 수행합니다. NTFS 마운트에서 직접 실행하지 않습니다.

## PR 전 확인

```bash
python -m pytest -q
python -m ruff check .
python -m mypy src/mois
```

- 문서가 한국어로 유지되는지 확인
- pre-commit hook이 통과하는지 확인 (`pre-commit run --all-files`)

## live 테스트

실제 API 호출 테스트는 기본 테스트에 섞지 않습니다. 인증키가 필요한 테스트는 `DATA_GO_KR_SERVICE_KEY` 환경변수를 사용하고 `@pytest.mark.live`를 붙입니다.

## 카탈로그 변경

공식 첨부자료가 바뀌면 다음을 함께 갱신합니다.

- `src/mois/catalog.py`
- `docs/api-list.md`
- `docs/file-downloads.md`
- `docs/response-fields.md`
- 관련 테스트의 기대 개수

## 의사결정 기록

아키텍처나 설계에 영향을 주는 결정을 했다면 `docs/decisions.md`에 ADR을 추가합니다.

## 변경 이력

사용자 가시 변경이 있으면 `CHANGELOG.md`에 항목을 추가합니다.
