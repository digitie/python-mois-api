from __future__ import annotations

import asyncio
import io
import logging
import os
import threading
from pathlib import Path
from urllib.parse import quote

import httpx
import pytest

from mois import (
    AsyncTokenBucket,
    EffectiveRustfsConfig,
    LocalDataFileClient,
    MoisClient,
    RustfsClient,
)
from mois._file_io import run_file_io
from mois._http import AsyncHttpxTransport
from mois.exceptions import MoisError


class CountingBucket(AsyncTokenBucket):
    def __init__(self) -> None:
        super().__init__(100000)
        self.calls = 0

    async def acquire(self) -> None:
        await super().acquire()
        self.calls += 1


def envelope(value: str = "0010") -> dict:
    return {
        "response": {
            "header": {"resultCode": "00"},
            "body": {
                "items": {"item": [{"MNG_NO": value}]},
                "totalCount": 1,
            },
        }
    }


def config() -> EffectiveRustfsConfig:
    return EffectiveRustfsConfig(
        True, "https://rustfs.test", "mois", "prefix", "us-east-1", True, "access", "secret"
    )


async def test_shared_budget_counts_retry_redirect_debug_files_and_rustfs(
    tmp_path: Path, monkeypatch
) -> None:
    budget = CountingBucket()
    urls = []

    def handler(request: httpx.Request) -> httpx.Response:
        urls.append(request.url)
        if len(urls) == 1:
            return httpx.Response(503)
        if len(urls) == 2:
            return httpx.Response(302, headers={"location": "/final"})
        if request.url.host == "file.test":
            return httpx.Response(200, content=b"MNG_NO\n0010\n")
        if request.url.host == "rustfs.test":
            return httpx.Response(200, headers={"etag": '"etag"'})
        return httpx.Response(200, json=envelope())

    monkeypatch.setattr("mois._http._retry_delay", lambda *args: 0)
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        async with (
            MoisClient("KEY", session=session, rate_limiter=budget) as api,
            LocalDataFileClient(
                session=session, base_url="https://file.test", rate_limiter=budget
            ) as files,
            RustfsClient(config(), session=session, rate_limiter=budget) as storage,
        ):
            assert (await api.request("hospitals")).items[0]["MNG_NO"] == "0010"
            assert (await api.debug_request("hospitals")).error is None
            content = await files.download_bytes("hospitals")
            assert content.startswith(b"MNG_NO")
            path = tmp_path / "hospital.csv"
            path.write_bytes(content)
            assert await storage.put_file("prefix/hospital.csv", path) == "etag"
        assert not session.is_closed
    assert budget.calls == len(urls) == 9


async def test_retry_retains_redirect_override(monkeypatch) -> None:
    statuses = iter([503, 302])
    budget = CountingBucket()
    monkeypatch.setattr("mois._http._retry_delay", lambda *args: 0)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(next(statuses), headers={"location": "/next"})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=True
    ) as session:
        transport = AsyncHttpxTransport(client=session, rate_limiter=budget)
        response = await transport.get("https://example.test/", follow_redirects=False)
        assert response.status_code == 302
        assert budget.calls == 2


async def test_repeated_cancel_drains_file_worker_before_return() -> None:
    started, release, finished = threading.Event(), threading.Event(), threading.Event()

    def worker() -> None:
        started.set()
        release.wait(timeout=5)
        finished.set()

    task = asyncio.create_task(run_file_io(worker))
    try:
        assert await asyncio.to_thread(started.wait, 2)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert not finished.is_set()
    finally:
        release.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert finished.is_set()


async def test_debug_model_error_and_httpx_log_mask_actual_key() -> None:
    secret = "synthetic/key+value"
    output = io.StringIO()
    logger = logging.getLogger("httpx")
    handler = logging.StreamHandler(output)
    old_level = logger.level
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    responses = iter(
        [
            httpx.Response(200, json=envelope(secret)),
            httpx.Response(
                200, json={"response": {"header": {"resultCode": secret, "resultMsg": secret}}}
            ),
        ]
    )
    try:
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(lambda _: next(responses))) as raw,
            MoisClient(secret, session=raw) as client,
        ):
            run = await client.debug_request("hospitals")
            assert run.error is None
            assert isinstance(run.parsed.items, tuple)
            assert secret not in repr(run.to_dict())
            with pytest.raises(MoisError) as error:
                await client.request("hospitals")
            assert secret not in repr(error.value.args)
            assert secret not in str(error.value.result_code)
        assert secret not in output.getvalue()
        assert quote(secret, safe="") not in output.getvalue()
    finally:
        logger.removeHandler(handler)
        logger.setLevel(old_level)


async def test_owned_pool_closes_and_closed_client_sends_nothing() -> None:
    client = MoisClient("KEY")
    assert client.transport._client is None
    await client.aclose()
    with pytest.raises(RuntimeError, match="closed"):
        await client.request("hospitals")
    assert client.transport._client is None


async def test_actual_override_key_and_unbound_response_debug() -> None:
    actual = "override/key+value"

    class AsyncSession:
        async def get(self, _url, **kwargs):
            assert kwargs["params"]["serviceKey"] == actual
            return httpx.Response(200, json=envelope(actual))

    async with MoisClient("configured", session=AsyncSession()) as client:
        run = await client.debug_request("hospitals", params={"serviceKey": actual})
        assert run.error is None
        assert actual not in repr(run.to_dict())
        assert run.parsed.items[0]["MNG_NO"] == "<REDACTED>"


async def test_sync_session_rejected_before_call() -> None:
    class SyncSession:
        def get(self, *_args, **_kwargs):
            pytest.fail("sync session was called")

    with pytest.raises(TypeError, match="async"):
        MoisClient("KEY", session=SyncSession())
    with pytest.raises(TypeError, match="async"):
        LocalDataFileClient(session=SyncSession())


async def test_digest_auth_rejected_without_send_or_token() -> None:
    budget = CountingBucket()
    async with (
        httpx.AsyncClient(
            auth=httpx.DigestAuth("user", "password"),
            transport=httpx.MockTransport(lambda _: pytest.fail("sent")),
        ) as raw,
        MoisClient("KEY", session=raw, rate_limiter=budget) as client,
    ):
        with pytest.raises(TypeError, match="Auth"):
            await client.request("hospitals")
    assert budget.calls == 0


async def test_landing_failure_stops_download() -> None:
    budget = CountingBucket()
    async with (
        httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(403))) as raw,
        LocalDataFileClient(session=raw, rate_limiter=budget) as client,
    ):
        with pytest.raises(MoisError, match="landing: HTTP 403"):
            await client.download_bytes("hospitals")
    assert budget.calls == 1


@pytest.mark.live
async def test_live_localdata_hospital_download(tmp_path: Path) -> None:
    if os.getenv("MOIS_RUN_LIVE") != "1":
        pytest.skip("MOIS_RUN_LIVE=1일 때만 실제 다운로드를 실행합니다")
    async with LocalDataFileClient(timeout=60, max_rps=2) as files:
        path = await files.download("hospitals", tmp_path / "hospitals.csv", org_code="3000000")
        rows = await files.load_file(path, slug="hospitals")
        assert rows
        assert any(row.management_number for row in rows)
