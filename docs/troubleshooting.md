# 문제 해결

## OpenAPI resultCode가 30 또는 31입니다

서비스키가 등록되지 않았거나 만료된 상태입니다. 공공데이터포털 마이페이지에서 해당 API 활용신청 상태와 디코딩 서비스키를 확인합니다.

## 조건을 넣었는데 결과가 없습니다

다음 항목을 먼저 확인합니다.

- 날짜 형식은 `YYYYMMDD` 또는 `YYYYMMDDHHMMSS`인지
- 조건 연산자는 `EQ`, `GTE`처럼 붙임1 형식과 맞는지
- 이력조회는 `BASE_DATE`와 `OPN_ATMY_GRP_CD` 조합이 필요한지
- 증분조회 기준이 `DAT_UPDT_PNT`인지 `LAST_MDFCN_PNT`인지

## localdata 파일 다운로드가 403입니다

localdata는 단순 다운로드 URL 직접 호출을 막는 경우가 있습니다. `LocalDataFileClient`는 안내 페이지 GET과 다운로드 제한 확인을 먼저 수행합니다. 직접 구현할 때도 같은 순서를 지킵니다.

## CSV 한글이 깨집니다

인허가정보 파일은 CP949 CSV가 기본입니다. `load()`는 자동 감지하지만 직접 읽는다면 다음처럼 읽습니다.

```python
text = content.decode("cp949")
```

## 좌표가 이상합니다

localdata 인허가정보 좌표는 WGS84가 아니라 EPSG:5174입니다. `pymois`는 원본 `CRD_INFO_X`, `CRD_INFO_Y`를 보존하고 `WGS84_LON`, `WGS84_LAT`를 추가합니다. 지도에 표시할 때는 WGS84 값을 사용합니다.

## 응답 필드가 문서와 다릅니다

붙임3은 기존 LOCALDATA 그룹별 항목과 신규 공공데이터포털 업종별 API 항목의 매핑 참고자료입니다. 업종별로 제공 여부가 다를 수 있으므로 특정 업종에서 필드가 없을 수 있습니다. 전체 매핑은 `docs/response-fields.md`와 `list_response_fields(include_deleted=True)`로 확인합니다.
