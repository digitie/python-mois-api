# 비동기·TPS 검증 결과

2026-09-14, 독립 적대적 리뷰 2인 승인 후 live E2E를 실행했다.

- 기본 pytest: 94 passed, 14 subtests, opt-in live 3 skipped. 기본 실행은 외부 API를 호출하지 않는다.
- mypy 20개 소스 파일, 전체 ruff, compileall 통과.
- 리뷰 A: 독립 14개 재현 통과. 반복 취소와 파일 종료, 재시도/리다이렉트 설정 유지,
  세션 소유권, RustFS 파일 핸들 및 서명, 진단 모델과 실제 override 키/HTTPX 로그 마스킹 확인.
- 리뷰 B: 관련 회귀 32개와 TPS 회귀 9개, 문서 원문 예제 19개 실행 통과.
  195개 카탈로그, CP949, 좌표 원본, 선행 0, DB UPSERT/commit/rollback/소스 종료 확인.
- live 파일: 종로구(`org_code=3000000`) 병원 CSV 다운로드와 파싱 **1 passed**.
- live OpenAPI: 같은 원격의 `python-krmois-api` 로컬 설정을 사용했으나
  `http://apis.data.go.kr/1741000/hospitals/info`가 **HTTP 403**, **1 failed**.
  조회 실패 뒤 실행될 디버그 호출은 도달하지 않았다. 실패를 데이터 검증 성공으로 계산하지 않는다.
- 195개 전체 다운로드와 RustFS 실제 업로드는 이번 live 범위에 포함하지 않았다.

새 403은 사용자에게 보고했으며 별도 판단 전까지 머지를 보류한다.

기존 범위의 제한: 외부 지오코더 검증은 EPSG:4326 입력의 각도 거리를 미터로 환산하지 않는
기존 문제가 있다. 이번 비동기 전환에서는 좌표 계산 정책을 변경하지 않았다.
