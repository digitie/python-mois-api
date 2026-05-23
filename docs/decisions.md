# 의사결정 기록 (ADR)

아키텍처나 설계에 영향을 주는 결정을 역시간순으로 기록한다.

---

## ADR-001: 개발 프로세스 표준화

- **일시**: 2026-05-23
- **결정**: `python-kraddr-geo` 프로젝트의 개발 방식을 도입한다.
- **맥락**: 프로젝트 규모가 커지면서 일관된 개발 프로세스, DO NOT 룰, 작업 후 체크리스트, ADR 기록, pre-commit hook이 필요해졌다.
- **결과**:
  - `AGENTS.md`에 지시 우선순위, DO NOT 룰, 작업 후 체크리스트 추가
  - `SKILL.md`에 DO NOT 룰, 도메인 어휘 추가
  - `CONTRIBUTING.md`에 작업 전 필독 목록, ADR 프로세스 추가
  - `.pre-commit-config.yaml`에 ruff, mypy hook 추가
  - `pyproject.toml`에 ruff lint 규칙 확대
  - `.gitignore`에 `.env` 패턴 추가
