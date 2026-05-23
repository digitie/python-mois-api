# python-mois-api 유지보수 스킬

이 스킬은 `python-mois-api` 저장소에서 행정안전부 지방행정 인허가정보 API와 localdata 파일 다운로드 기능을 수정할 때 사용합니다.

## 1. 핵심 맥락

- 공공데이터포털 공지 `NOTICE_0000000004566`의 붙임2가 OpenAPI URL 목록입니다.
- 붙임3이 응답변수 매핑표입니다.
- localdata 파일 다운로드 페이지는 업종별 인허가정보 파일 목록을 제공합니다.
- OpenAPI 업종은 195개이며 `info`, `history` 두 URL이 있습니다.
- localdata 인허가정보 파일 다운로드도 195개입니다.

## 2. 구현 규칙

- `MoisClient`는 slug 기반 공통 호출을 유지합니다.
- `LocalDataFileClient`는 안내 페이지 GET, 다운로드 제한 확인, 실제 다운로드 순서를 유지합니다.
- CSV 로더는 CP949, 날짜/시각, 숫자, 좌표 변환을 유지합니다.
- EPSG:5174 원본 좌표는 보존하고 WGS84 값을 추가합니다.
- 삭제된 응답변수는 기본 목록에서 제외합니다.

## 3. 테스트 규칙

- 기본 테스트는 네트워크를 사용하지 않습니다.
- 실제 API 호출은 `@pytest.mark.live`로 분리합니다.
- 카탈로그 개수 테스트를 수정할 때는 공식 출처가 바뀐 경우인지 먼저 확인합니다.

## 4. 절대 하지 말 것 (DO NOT)

1. **API 목록 손 복사 금지** — `src/mois/catalog.py`와 `tools/generate_docs.py`를 기준으로 관리합니다. 목록을 직접 손으로 옮기지 않습니다.
2. **좌표 원본 덮어쓰기 금지** — EPSG:5174 원본은 보존하고 WGS84를 추가합니다. 원본 좌표를 덮어쓰지 않습니다.
3. **빈 값을 0으로 치환 금지** — 의미 없는 빈 문자열은 `None`입니다. 숫자 0으로 바꾸지 않습니다.
4. **localdata 다운로드 순서 무시 금지** — 안내 페이지 GET → 다운로드 제한 확인 → 실제 다운로드 순서를 지킵니다.
5. **단순 전달용 래퍼 금지** — wrapper, 장기 호환 alias, 임시 facade를 만들지 않습니다.
6. **삭제 응답변수 기본 포함 금지** — 붙임3의 삭제 항목은 기본 목록에서 제외합니다.
7. **네트워크 사용 기본 테스트 금지** — live 테스트는 `@pytest.mark.live`로 분리합니다.
8. **외부 API 키 커밋 금지** — `MOIS_SERVICE_KEY`는 환경변수로만 전달합니다.
9. **전체 flat table 금지** — 195개 업종의 특수 칼럼을 하나의 flat table에 모두 펼치지 않습니다.
10. **확인되지 않은 항목 추정 금지** — PDF와 실제 카탈로그 개수가 다를 때 확인되지 않은 항목을 코드에 넣지 않습니다.

## 5. 도메인 어휘

| 용어 | 설명 |
|------|------|
| slug | 업종 식별 문자열 (예: `hospitals`, `restaurants`) |
| MNG_NO | 관리번호 — 인허가 레코드의 고유 식별자 |
| DAT_UPDT_PNT | 개방데이터 보강 수정 시점 (증분조회 기본 필드) |
| LAST_MDFCN_PNT | 원천데이터 수정 시점 |
| EPSG:5174 | KATEC 좌표계 — localdata CSV의 원본 좌표 |
| WGS84 / EPSG:4326 | GPS 좌표계 — `(lon, lat)` 순서 |
| localdata | `file.localdata.go.kr`에서 제공하는 인허가정보 파일 다운로드 |
| 붙임2 | OpenAPI URL 목록 엑셀 |
| 붙임3 | 응답변수 매핑표 엑셀 |

## 6. 문서 규칙

- README와 `docs/*`는 한국어로 작성합니다.
- 목록 문서는 `tools/generate_docs.py`로 생성합니다.
- 문서 생성 후 UTF-8로 깨지지 않았는지 확인합니다.

## 7. 작업 후 체크리스트

- [ ] `python -m pytest -q` 통과
- [ ] `python -m ruff check .` 통과
- [ ] `python -m mypy src/mois` 통과
- [ ] 의사결정이 있었다면 `docs/decisions.md`에 ADR 추가
- [ ] 사용자 가시 변경이면 `CHANGELOG.md` 갱신
- [ ] OpenAPI 목록 변경은 `src/mois/catalog.py`, `docs/api-list.md`, `docs/response-fields.md` 함께 갱신
