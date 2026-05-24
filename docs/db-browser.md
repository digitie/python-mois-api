# DB 브라우저 웹앱

`packages/mois-debug-ui`는 `mois`로 SQLite/SpatiaLite에 적재한 인허가 DB를 조회하는 웹앱입니다. 백엔드는 FastAPI, 프론트엔드는 React와 Tailwind CSS 기반입니다.

## 구성

| 경로 | 설명 |
|---|---|
| `packages/mois-debug-ui/src/mois_debug_ui/backend` | FastAPI API 서버 |
| `packages/mois-debug-ui/frontend` | Vite + React + Tailwind CSS 프론트엔드 |

백엔드는 `mois_place_master`, `mois_place_detail` 테이블을 읽습니다. DB 파일 경로는 `MOIS_SQLITE_PATH` 환경변수로 전달합니다. FastAPI 라우트와 조회 저장소는 `sqlite+aiosqlite` 기반 SQLAlchemy 2 `AsyncEngine`/`AsyncSession`을 사용합니다. 스키마 생성과 대량 파일 적재는 배치 작업 성격이라 기존 동기 SQLAlchemy 경로를 유지합니다.

SQLite 접근은 SQLAlchemy 2와 선택적 SpatiaLite를 기준으로 합니다. 런타임 조회 경로에서 GeoAlchemy2, GeoPandas, Shapely는 사용하지 않습니다. 좌표는 일반 컬럼 `lat`, `lon`, WKT `geom_wkt`, 그리고 SpatiaLite가 가능할 때 `geom` 컬럼으로 보존합니다.

## Windows SpatiaLite 준비

Windows에서 SpatiaLite를 사용하려면 `mod_spatialite.dll`과 의존 DLL이 같은 폴더에 있어야 합니다. 로컬 검증 환경은 공식 Windows amd64 바이너리를 `F:\dev\spatialite\bin`에 풀어 사용합니다.

```powershell
$env:PATH = "F:\dev\spatialite\bin;$env:PATH"
$env:PROJ_LIB = "F:\dev\spatialite\bin"
```

확장을 로드할 수 없는 환경에서도 `lat`, `lon`, `geom_wkt`와 일반 인덱스로 조회 서버는 동작합니다. `/api/health`의 `spatialiteEnabled` 값으로 현재 상태를 확인합니다.

## 원본 다운로드 파일 보관

내려받은 원본 localdata 파일은 `artifacts/localdata/` 아래에 저장합니다. `artifacts/`는 `.gitignore`에 포함되어 있으므로 원본 데이터가 git에 노출되지 않습니다.

```text
artifacts/localdata/hospitals_info.bin
```

## 다운로드 파일 적재

이미 내려받은 localdata CSV/ZIP 파일은 `mois_debug_ui.backend.load_sqlite` CLI로 적재합니다. 파일은 CP949 CSV 또는 ZIP을 모두 처리하며, 좌표는 기존 `mois` 로더를 거쳐 WGS84 `(lat, lon)`와 WKT로 저장합니다.

```powershell
$env:MOIS_SQLITE_PATH = "F:\dev\python-mois-api\artifacts\mois.sqlite"
python -m mois_debug_ui.backend.load_sqlite --file artifacts/localdata/hospitals_info.bin --slug hospitals --replace-slug
```

asyncio 흐름에서는 같은 로컬 파일 적재를 `aload_local_file_to_sqlite()`로 실행할 수 있습니다.

```python
from mois_debug_ui.backend.load_sqlite import aload_local_file_to_sqlite

loaded = await aload_local_file_to_sqlite(
    database_path="artifacts/mois.sqlite",
    file_path="artifacts/localdata/hospitals_info.bin",
    slug="hospitals",
    replace_slug=True,
)
```

전체 195개 인허가 파일을 모두 저장하고 적재할 때는 운영 스크립트를 사용합니다.

```powershell
$env:MOIS_SQLITE_PATH = "F:\dev\python-mois-api\artifacts\mois.sqlite"
python -m tools.load_all_localdata_to_sqlite --output-dir artifacts/localdata --progress-path artifacts/load_all_localdata_sqlite_progress.jsonl --replace-slug --continue-on-error --batch-size 1000
```

진행 상황은 JSONL 형식으로 남습니다. 원본 파일만 먼저 저장하려면 `--download-only`를 붙입니다.
SQLite 파일 크기를 줄이기 위해 컬럼으로 승격한 필드는 상세 JSON에 중복 저장하지 않습니다.

## 백엔드 실행

```powershell
pip install -e ".[dev]"
pip install -e packages/mois-debug-ui

$env:MOIS_SQLITE_PATH = "F:\dev\python-mois-api\artifacts\mois.sqlite"
$env:MOIS_WEB_HOST = "127.0.0.1"
$env:MOIS_WEB_PORT = "8611"
python -m mois_debug_ui.backend
```

주요 API:

| API | 설명 |
|---|---|
| `GET /api/health` | 서버, DB 설정, SpatiaLite 로드 상태 |
| `GET /api/stats` | 전체 건수, 영업 건수, 좌표 보유 건수, 업종 요약 |
| `GET /api/services` | DB에 적재된 업종 목록과 건수 |
| `GET /api/places` | 인허가 레코드 검색/필터/페이지 조회 |
| `GET /api/places/{place_id}` | 마스터와 상세 JSON 데이터 조회 |

`/api/places` 쿼리 파라미터:

| 파라미터 | 설명 |
|---|---|
| `q` | 사업장명, 주소, 관리번호 검색어 |
| `service_slug` | 업종 slug |
| `category` | 인허가 분류 |
| `is_open` | `true` 또는 `false` |
| `detail_status_code` | 상세 영업상태 코드 |
| `business_type_name` | 업태명 |
| `subtype_name` | 업종별 세부 업종명 통합값 |
| `sales_method_name` | 전자상거래 등 판매 방식 |
| `limit` | 1~200 |
| `offset` | 페이지 시작 위치 |

## 프론트엔드 실행

```powershell
cd packages\mois-debug-ui\frontend
npm install
npm run dev
```

개발 서버는 기본적으로 `http://localhost:8610`에서 뜨고, Vite proxy가 `/api` 요청을 `http://127.0.0.1:8611`으로 보냅니다. Kakao Maps JavaScript SDK 도메인도 `http://localhost:8610`에 맞춥니다.

백엔드 주소가 다르면 `.env.local` 또는 실행 환경에 다음 값을 둡니다.

```powershell
$env:VITE_API_BASE_URL = "http://127.0.0.1:8611"
$env:VITE_KAKAO_MAP_APP_KEY = "Kakao JavaScript 앱 키"
```

## 빌드 후 백엔드에서 함께 서빙

```powershell
cd packages\mois-debug-ui\frontend
npm run build

cd ..\..\..
$env:MOIS_SQLITE_PATH = "F:\dev\python-mois-api\artifacts\mois.sqlite"
python -m mois_debug_ui.backend
```

`packages/mois-debug-ui/frontend/dist`가 있으면 FastAPI가 빌드된 프론트엔드를 함께 서빙합니다.

## 화면에서 확인할 수 있는 것

- 전체 적재 건수, 영업 중 건수, 좌표 보유 건수, 업종 수
- 분류/업종/영업 상태/검색어 필터
- 사업장명, 관리번호, 주소, WGS84 좌표 `(lat, lon)`, 수정일
- 상세 패널의 Kakao 지도 기반 위치 확인
- 레코드별 `specific_data`, 재구성된 `recordData`, 비승격 원본 필드 `rawData`

## 주의

- `MOIS_SQLITE_PATH`가 없으면 API는 503을 반환합니다.
- 이 앱은 조회용입니다. DB 수정이나 재적재 기능은 CLI로 수행합니다.
- 대량 테이블에서는 검색어 없는 전체 조회보다 업종/분류 필터를 함께 쓰는 것이 좋습니다.
