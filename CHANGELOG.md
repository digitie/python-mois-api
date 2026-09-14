# 변경 이력

이 문서는 [Keep a Changelog](https://keepachangelog.com/) 형식을 따른다.

## [Unreleased]

- MoisClient/LocalDataFileClient/RustfsClient와 외부 지오코딩 검증을 비동기 전용으로 통합. Async 접두사·aio 팩터리·동기 transport 제거.
- 공통 AsyncTokenBucket의 max_rps/rate_limiter로 요청·재시도·리다이렉트·파일 다운로드·RustFS의 TPS를 제어.
- sync_localdata_source_db는 AsyncSession을 받는 비동기 함수로 변경. 파일 취소/세션 소유권 및 디버그 키 마스킹 보강.

- 카탈로그 기반 Streamlit 디버그 UI(`examples/streamlit_debug_ui.py`) 추가: `python-khoa-api` 템플릿에
  맞춰 Data source → Category → API 3단 계단식 선택, `required_params`/`optional_params` 메타데이터
  기반 파라미터 폼 자동 생성(업종별 하드코딩 분기 없음), 고정 6개 탭(Raw Response/Pydantic
  Model/Processed Result/Validation Errors/Debug Trace/Fixture·Testcase), 구조화 에러 표시,
  `save_fixture()` 실 저장 기능 포함(ADR-010)
- `OpenApiService`에 `required_params`/`optional_params` 파라미터 위젯 메타데이터 필드 추가, 이를
  평평한 dict로 반환하는 `get_api_catalog()`/`get_api_catalog_entry()` 추가
- `mois.debug.error_to_dict()`가 `MoisError` 계열 예외의 `result_code`를 함께 반환하도록 개선
- `pyproject.toml`에 `debug-ui = ["pandas>=2", "streamlit>=1.36"]` optional dependency 추가

## 0.1.0

- 지방행정 인허가정보 OpenAPI 195개 업종과 이력조회 195개 URL 카탈로그 추가
- 195개 업종별 공공데이터포털 활용신청 링크와 증분조회 카탈로그 추가
- `MoisClient` 공통 호출, 조건 파라미터, JSON/XML 응답 파서 추가
- `get_updated`, `iter_updated`, `get_updated_{slug}`, `iter_updated_{slug}`, `get_history_at`, `iter_history_at` 증분/이력 조회 편의 메서드 추가
- localdata 인허가정보 파일 다운로드 195개 카탈로그 추가
- `LocalDataFileClient` 다운로드/로드 API 추가
- CP949 CSV, 날짜/시각, 숫자, EPSG:5174 좌표를 Python 타입과 WGS84로 변환
- `KatecPoint`, `Wgs84Point`, `StationCoordinates` 좌표 값 객체와 enum/type 별칭 추가
- Pydantic, SQLAlchemy 2 기반 SQLite/SpatiaLite 적재 모델 추가
- 법정동코드, 도로명코드, 건물관리번호 연계 후보 문서화
- 여행 플래너 활용 아키텍처, DB 스키마, UPSERT 기반 증분 동기화 문서 추가
- API/파일/응답변수/증분 OpenAPI 신청 링크 목록 문서화
- 네트워크 없는 단위 테스트 추가
- 4인 전문 리뷰어 서브에이전트의 적대적 코드 리뷰로 발견·검증된 버그 수정: CSV 좌표 이상값으로 인한 전체 로드 중단, `LocalDataRecord.is_open`의 "영업정지" 오분류, DB 왕복 시 `PlaceRecord.data` 필드 유실, `iter_updated`/`get_updated`의 tz-aware datetime KST 미변환, `debug_request()`의 `service_key` 오류 메시지 유출, 게이트웨이 인증 오류(XML `cmmMsgHeader`) 무시, `iter_records` 무한 루프 가능성, 비동기 파일 클라이언트의 이벤트 루프 블로킹 등
- GitHub Actions CI 워크플로(`lint`/`typecheck`/`test`) 추가
- `python-kraddr-geo` → `kor-travel-geo` 리네임과 v2 API(`CandidateV2`) 반영: 깨져 있던
  `tests/test_geocoding.py` 3건 수정(fake 지오코더가 `AddressGeocoder` 계약대로 `GeocodingCandidate`를
  반환하도록 변경), `docs/integration-with-kor-travel-geo.md` 신규 작성(GPL-3.0 라이선스 경계, v2
  adapter 예시 포함), ADR-002/004/007/009와 `AGENTS.md`/`README.md`/`docs/repeated-mistakes.md`의 옛 이름·API
  참조 정정
