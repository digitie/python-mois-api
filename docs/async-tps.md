# 비동기 API와 공통 TPS

MoisClient, LocalDataFileClient, RustfsClient는 비동기 전용이다. 모든 네트워크 조회와
디버그에는 await, 페이지·파일 행 순회에는 async for, 세션 종료에는 async with 또는
await client.aclose()를 사용한다. Async 접두사 클래스와 aio 팩터리는 제거했다.
기존 195개 업종 카탈로그·조건·CP949·빈 값·날짜·좌표 원본 보존 규칙은 유지한다.

```python
import asyncio
from mois import AsyncTokenBucket, MoisClient, LocalDataFileClient


async def main() -> None:
    budget = AsyncTokenBucket(2, capacity=1)
    async with (
        MoisClient.from_env(rate_limiter=budget) as client,
        LocalDataFileClient(rate_limiter=budget) as files,
    ):
        rows = await client.get_hospitals(num_of_rows=1)
        print(rows)
        async for record in files.iter_hospitals(org_code="3610000"):
            print(record.business_name)


asyncio.run(main())
```

기본 max_rps=5.0이다. AsyncTokenBucket의 기본 capacity=max(1, max_rps)는 초기 burst를
허용한다. 일정한 송신 간격은 capacity=1로 지정한다. 주입한 rate_limiter는 max_rps보다
우선하며, 여러 클라이언트에 같은 버킷을 전달하면 예산을 합산한다. 한 이벤트 루프에서
사용하고, 대기 취소는 토큰을 소비하지 않는다. 일일 다운로드/API 쿼터는 별도다.

OpenAPI 일반 조회·디버그·페이지·재시도·리다이렉트, localdata 안내 페이지·제한 확인·
다운로드 각각에 토큰을 사용한다. 기존 429/500/502/503/504와 HTTPX 네트워크 오류 재시도
정책을 유지한다. Retry-After가 8초를 초과하면 즉시 응답을 반환한다. 401/403은 재시도하지 않는다.
Digest/custom Auth의 내부 추가 송신은 사전 거부한다. BasicAuth/noAuth를 지원한다.
사용자 정의 transport 내부에서 발생하는 추가 송신은 해당 transport의 책임이다.

내부 HTTP 세션은 첫 요청에 생성해 종료 시 닫는다. 주입한 비동기 세션/transport는
호출자가 닫는다. AsyncHttpxTransport를 직접 주입할 때는 그 transport의 버킷을 공유하며,
별도 rate_limiter를 지정한다면 같은 인스턴스여야 한다. 닫힌 클라이언트는 추가 송신을 거부한다.
파일 다운로드 취소 시 진행 중인 파일 작업을 마친 후 응답과 파일을 닫는다.

RustFS는 HEAD/PUT마다 같은 버킷을 사용하고, download_to_rustfs는 다운로드 클라이언트의
버킷을 넘긴다. SigV4는 토큰 확보 뒤 서명한다. 서명된 PUT의 자동 재시도·리다이렉트는
하지 않는다. RustFS는 session auth를 허용하지 않으며 내부 세션을 재사용한다.

외부 지오코더 검증은 await validate_address_geocoding_probe(...) 하나로 통합했다.
AddressGeocoder의 두 메서드는 async이며, 외부 지오코더 자체 TPS 설정을 따른다.
네트워크 다운로드를 DB로 연결하는 sync_localdata_source_db는 async이고 AsyncSession을
받는다. sync는 데이터 동기화라는 의미다. 기존 로컬 파싱·코드표·모델 변환·fixture 저장과
독립 SQLAlchemy 배치 유틸리티는 일반 함수다. AsyncSession.run_sync/run_sync 연결을 이용한다.

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from mois import Base, LocalDataFileClient, sync_localdata_source_db


async def main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///mois.sqlite")
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with AsyncSession(engine) as session, LocalDataFileClient() as files:
            result = await sync_localdata_source_db(
                session, files, service_slugs=("hospitals",), batch_size=1000,
            )
            print(result.scanned_count)
    finally:
        await engine.dispose()


asyncio.run(main())
```

SQLite의 AsyncEngine 사용에는 aiosqlite가 필요하다. 로컬 파일/DB 배치 처리는 외부 HTTP
TPS에 포함하지 않는다. CLI와 Streamlit 예제는 최상위에서만 asyncio.run으로 진입한다.
진단은 원문 파싱 뒤 실제 서비스키와 인코딩된 키를 마스킹한다.
