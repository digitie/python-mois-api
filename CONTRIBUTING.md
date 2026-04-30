# 기여 안내

`pymois`에 기여할 때는 공식 자료와 실제 응답 사이의 차이를 분리해서 기록해 주세요.

## 개발 환경

```bash
pip install -e ".[dev]"
python -m pytest
```

## PR 전 확인

- `python -m pytest`
- `python -m ruff check .`
- `python -m mypy pymois`
- 문서가 한국어로 유지되는지 확인

## live 테스트

실제 API 호출 테스트는 기본 테스트에 섞지 않습니다. 인증키가 필요한 테스트는 `MOIS_SERVICE_KEY` 환경변수를 사용하고 `@pytest.mark.live`를 붙입니다.

## 카탈로그 변경

공식 첨부자료가 바뀌면 다음을 함께 갱신합니다.

- `pymois/catalog.py`
- `docs/api-list.md`
- `docs/file-downloads.md`
- `docs/response-fields.md`
- 관련 테스트의 기대 개수
