# python-mois-api

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![MIT 라이선스](https://img.shields.io/badge/License-MIT-blue.svg)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

`python-mois-api`는 행정안전부 지방행정 인허가정보를 Python에서 다루기 위한 라이브러리입니다. 설치
패키지 이름은 `python-mois-api`, import 패키지 이름은 `mois`입니다. 공공데이터포털 지방행정
인허가정보 OpenAPI 195종과 `file.localdata.go.kr`의 인허가정보 파일 다운로드 195종을 같은 slug로
카탈로그화해 비동기 전용 클라이언트로 제공합니다. 주소 정규화와 정/역 지오코딩은 담당하지 않고, 별도
라이브러리 [`kor-travel-geo`](https://github.com/digitie/kor-travel-geo)(구 `python-kraddr-geo`,
GPL-3.0-only)에 위임합니다(ADR-002).

다음 릴리스에 포함될 변경 사항은 [`CHANGELOG.md`](CHANGELOG.md)의 `[Unreleased]` 섹션에서 확인할 수
있습니다.

## 제공 표면

| 표면 | 진입점 | 설명 |
|------|--------|------|
| OpenAPI 클라이언트 | `from mois import MoisClient` | 195개 업종 조회/이력조회/증분조회, 동기와 `MoisClient()` 비동기 |
| 파일 다운로드 클라이언트 | `from mois import LocalDataFileClient` | localdata 인허가정보 파일 195종 다운로드와 스트리밍 로드 |
| SQLite/SpatiaLite 적재 | `from mois import create_sqlite_schema, upsert_places` | 마스터-디테일 + JSON 컬럼 로컬 DB 모델과 증분 동기화 helper |
| 지오코딩 검증 helper | `validate_address_geocoding_probe` | `kor-travel-geo` 결과와 자체 좌표를 비교만 함(ADR-002) |
| DB 브라우저(별도 패키지) | `python -m mois_debug_ui.backend` | 내부 운영용 FastAPI + React 콘솔(`packages/mois-debug-ui`, ADR-007) |

## 먼저 읽을 문서

README는 입구 역할만 합니다. 세부 절차와 결정은 아래 문서를 정본으로 봅니다.

| 필요 정보 | 문서 |
|-----------|------|
| 설계 의사결정(ADR) | [`docs/decisions.md`](docs/decisions.md) |
| `kor-travel-geo`와의 통합 전략 | [`docs/integration-with-kor-travel-geo.md`](docs/integration-with-kor-travel-geo.md) |
| API 및 파일 다운로드 목록 | [`docs/api-list.md`](docs/api-list.md) |
| 증분 OpenAPI 목록과 신청 링크 | [`docs/incremental-openapi.md`](docs/incremental-openapi.md) |
| 파일 다운로드와 로드 API | [`docs/file-downloads.md`](docs/file-downloads.md) |
| 타입과 좌표 값 객체 | [`docs/types-and-coordinates.md`](docs/types-and-coordinates.md) |
| SQLite/SpatiaLite DB 적재 | [`docs/database.md`](docs/database.md) |
| DB 구조 정리 | [`docs/db-structure.md`](docs/db-structure.md) |
| SQLite/SpatiaLite 전환 상세 보고서 | [`docs/sqlite-spatialite-migration-report.md`](docs/sqlite-spatialite-migration-report.md) |
| JSON 필드 → 컬럼 승격 기준 | [`docs/json-field-promotion.md`](docs/json-field-promotion.md) |
| PostgreSQL/PostGIS 설계 이력(과거, 비현행) | [`docs/postgresql-postgis-history.md`](docs/postgresql-postgis-history.md) |
| DB 브라우저 웹앱 | [`docs/db-browser.md`](docs/db-browser.md) |
| 응답변수 매핑표 | [`docs/response-fields.md`](docs/response-fields.md) |
| 관광 관련 인허가 데이터 선별 목록 | [`docs/tourism-license-data.md`](docs/tourism-license-data.md) |
| 여행 플래너 활용 아키텍처 | [`docs/travel-planner-architecture.md`](docs/travel-planner-architecture.md) |
| 구현 메모 | [`mois-api.md`](mois-api.md) |
| 반복 실수 방지 | [`docs/repeated-mistakes.md`](docs/repeated-mistakes.md) |
| 테스트 기준 | [`docs/testing.md`](docs/testing.md) |
| 문제 해결 | [`docs/troubleshooting.md`](docs/troubleshooting.md) |

## 설치

```bash
pip install python-mois-api
```

개발 중인 저장소에서는 다음처럼 설치합니다. DB 브라우저 디버그 웹 UI(`packages/mois-debug-ui/`,
ADR-007)는 별도 패키지이므로 필요할 때만 함께 수정 가능 모드로 설치합니다.

```bash
pip install -e ".[dev]"
pip install -e packages/mois-debug-ui
```

195개 업종 OpenAPI를 카탈로그 기반으로 하나씩 호출해 보는 가벼운 Streamlit 디버그 UI는 별도
optional dependency로 설치합니다.

```bash
pip install -e ".[debug-ui]"
streamlit run examples/streamlit_debug_ui.py
```

공공데이터포털에서 지방행정 인허가정보 API 활용신청 후 받은 디코딩 서비스키를 환경변수로 전달합니다.

```bash
export DATA_GO_KR_SERVICE_KEY="공공데이터포털_서비스키"
```

```python
from mois import MoisClient

client = MoisClient.from_env()
```

## 예제

```python
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from mois import MoisClient


async def main() -> None:
    async with MoisClient.from_env() as client:
        changed = (await client.get_updated(
            "hospitals",
            datetime(2026, 5, 5, 0, 0, 0, tzinfo=ZoneInfo("Asia/Seoul")),
        ))
        for item in changed:
            print(item["MNG_NO"], item.get("BPLC_NM"))


asyncio.run(main())
```

이 예제는 `hospitals` 업종의 동기 증분조회만 다룹니다. 비동기 호출, 파일 다운로드, SQLite 적재, DB
브라우저는 위 "먼저 읽을 문서" 표의 각 문서를 참고하십시오.

## 검증

```bash
python -m pytest
python -m ruff check .
python -m mypy src/mois
```

기본 테스트는 실제 API를 호출하지 않습니다. 실제 호출 테스트를 추가할 때는 `@pytest.mark.live`를
붙이고 `DATA_GO_KR_SERVICE_KEY`가 있을 때만 실행되게 합니다.

## 참고 출처

- [공공데이터포털 공지 `NOTICE_0000000004566`](https://www.data.go.kr/bbs/ntc/selectNotice.do?pageIndex=1&originId=NOTICE_0000000004566&atchFileId=FILE_000000003615156&nttApiYn=Y&searchCondition2=2&searchKeyword1=%EC%9D%B8%ED%97%88%EA%B0%80)
- 붙임1. 공공데이터포털 지방행정 인허가정보 API 호출 예시.pdf
- 붙임2. 공공데이터포털 지방행정 인허가정보 API 호출 URL 목록.xlsx
- 붙임3. 지방행정 인허가정보의 제공항목(응답변수) 매핑테이블_20260407수정.xlsx
- https://file.localdata.go.kr/file/hospitals/info

## 디렉터리 개요

| 경로 | 역할 |
|------|------|
| `src/mois/client.py` | `MoisClient` OpenAPI 호출 |
| `src/mois/files.py` | `LocalDataFileClient` 파일 다운로드/로드 |
| `src/mois/catalog.py` | 195개 업종 OpenAPI/파일 카탈로그(자동 생성 기준, ADR-006) |
| `src/mois/db.py` | SQLite/SpatiaLite 적재 모델과 upsert/iterator(ADR-008) |
| `src/mois/geocoding.py` | `validate_address_geocoding_probe` 검증 helper(ADR-002) |
| `src/mois/models.py`, `coords.py`, `convert.py`, `parser.py` | 응답/좌표 값 객체와 변환 |
| `tests/` | 네트워크 없는 단위 테스트(fixture 재생). live 테스트는 `@pytest.mark.live` |
| `tools/` | 문서/카탈로그 생성, 전체 localdata 적재 운영 스크립트 |
| `examples/streamlit_debug_ui.py` | 카탈로그 기반 OpenAPI Streamlit 디버그 UI(`.[debug-ui]`, ADR-010) |
| `packages/mois-debug-ui/` | 별도 패키지 DB 브라우저(FastAPI + React, ADR-007) |
| `docs/` | ADR, API/파일 카탈로그, DB 구조, 통합 전략 문서 |

## 문서와 기여 규칙

- Markdown 문서는 한국어로 작성합니다. 코드 식별자, API 필드명, 명령어, URL, 제공자 원문 용어만
  원문 표기를 유지합니다.
- 작업 전 [`AGENTS.md`](AGENTS.md)와 [`docs/decisions.md`](docs/decisions.md)의 관련 ADR을 확인합니다.
- OpenAPI/파일 카탈로그는 `tools/generate_docs.py`로 `src/mois/catalog.py` 기준으로만 갱신합니다(손
  복사 금지, ADR-006).
- 사용자 가시 변경은 [`CHANGELOG.md`](CHANGELOG.md)에 기록합니다.

## 법적 고지

MIT 라이선스는 이 저장소에 포함된 소스 코드와 문서에만 적용됩니다. 자세한 조건은
[`LICENSE`](LICENSE)를 확인하십시오. 행정안전부 지방행정 인허가정보 OpenAPI와
`file.localdata.go.kr` 파일 다운로드는 공공데이터포털/행정안전부가 정한 이용약관과 재배포 조건을
따르며, 이 라이브러리는 그 데이터를 다루는 기술 도구일 뿐 데이터의 정확성이나 법적 효력을 보장하지
않습니다.

## 비동기 전용 호출과 TPS

공개 네트워크 클라이언트는 native async 하나로 통합했다.
`max_rps` 또는 공유 `AsyncTokenBucket`을 `rate_limiter=`에 전달한다.
기존 동기/비동기 병행 지침은 ADR-013로 대체했다. [호출·TPS·소유권·DB 예제](docs/async-tps.md)를 따른다.
