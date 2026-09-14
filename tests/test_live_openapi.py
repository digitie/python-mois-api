from __future__ import annotations

import os

import pytest

from mois import MoisClient


@pytest.mark.live
async def test_live_hospitals_first_page_and_debug() -> None:
    if os.getenv("MOIS_RUN_LIVE") != "1":
        pytest.skip("MOIS_RUN_LIVE=1일 때만 실제 API를 호출합니다")
    key = os.getenv("DATA_GO_KR_SERVICE_KEY")
    if not key:
        pytest.skip("DATA_GO_KR_SERVICE_KEY가 없습니다")
    async with MoisClient(key, timeout=30.0, max_rps=2.0) as client:
        rows = await client.get_hospitals(num_of_rows=1)
        assert rows
        run = await client.debug_request("hospitals", num_of_rows=1)
        assert run.error is None, run.error
        assert run.processed
