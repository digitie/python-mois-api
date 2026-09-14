"""httpx 기반 HTTP transport와 공통 응답 처리."""

from __future__ import annotations

import asyncio
import inspect
import logging
import math
import random
import re
from typing import Any, Protocol

import httpx

from ._httpx import send_after_token
from ._ratelimit import AsyncTokenBucket
from .exceptions import MoisRequestError, MoisServerError

DEFAULT_USER_AGENT = "python-mois-api/0.1 (+https://github.com/digitie/python-mois-api)"
RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
MAX_RETRY_DELAY = 8.0
HTTP_CLIENT_ERROR = httpx.HTTPError


class _KeyLogFilter(logging.Filter):
    """HTTPX의 요청 URL 로그에서 서비스키 쿼리를 제거합니다."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = re.sub(
            r"(?i)([?&]service_?key=)[^&\s\"']+", r"\1<REDACTED>", record.getMessage()
        )
        record.args = ()
        return True


logging.getLogger("httpx").addFilter(_KeyLogFilter())


class AsyncTransport(Protocol):
    """비동기 클라이언트가 사용하는 최소 HTTP transport 프로토콜."""

    async def get(self, url: str, **kwargs: Any) -> Any: ...

    async def aclose(self) -> None: ...


def raise_for_http_error(response: Any, context: str) -> None:
    """HTTP 상태코드를 mois 예외로 매핑합니다."""

    status = getattr(response, "status_code", None)
    if status is None or 200 <= int(status) < 400:
        return
    if int(status) >= 500:
        raise MoisServerError(f"{context}: HTTP {status}")
    raise MoisRequestError(f"{context}: HTTP {status}")


def _retry_delay(attempt: int, retry_after: float | None = None) -> float:
    if retry_after is not None:
        return retry_after
    delay = min(MAX_RETRY_DELAY, 0.5 * (2**attempt))
    return random.uniform(0, delay)


def _parse_retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    try:
        seconds = float(value)
    except ValueError:
        return None
    return seconds if math.isfinite(seconds) and seconds >= 0 else None


class AsyncHttpxTransport:
    """송신·재시도·리다이렉트가 같은 버킷을 사용하는 비동기 transport."""

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        retries: int = 2,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
        client: Any | None = None,
    ) -> None:
        if client is not None and not inspect.iscoroutinefunction(client.get):
            raise TypeError("session.get must be async")
        self.timeout = timeout
        self.retries = max(0, retries)
        self.rate_limiter = rate_limiter if rate_limiter is not None else AsyncTokenBucket(max_rps)
        self._client = client
        self._owns_client = client is None
        self.closed = False

    def _ready(self) -> Any:
        if self.closed:
            raise RuntimeError("transport is closed")
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={"User-Agent": DEFAULT_USER_AGENT},
                timeout=self.timeout,
                follow_redirects=True,
            )
        if isinstance(self._client, httpx.AsyncClient):
            auth = self._client.auth
            if auth is not None and type(auth) not in {httpx.Auth, httpx.BasicAuth}:
                raise TypeError("Digest/custom Auth may send unmetered requests")
        return self._client

    async def get(self, url: str, **kwargs: Any) -> Any:
        stream = bool(kwargs.pop("stream", False))
        timeout = kwargs.pop("timeout", self.timeout)
        follow = kwargs.pop("follow_redirects", None)
        self._ready()
        for attempt in range(self.retries + 1):
            await self.rate_limiter.acquire()
            client = self._ready()
            try:
                if isinstance(client, httpx.AsyncClient):
                    request = client.build_request("GET", url, timeout=timeout, **kwargs)
                    response = await send_after_token(
                        client, request, self.rate_limiter, stream=stream, follow_redirects=follow
                    )
                else:
                    options = dict(kwargs)
                    if follow is not None:
                        options["follow_redirects"] = follow
                    response = await client.get(url, stream=stream, timeout=timeout, **options)
            except httpx.TooManyRedirects:
                raise
            except httpx.HTTPError:
                if attempt >= self.retries:
                    raise
                await asyncio.sleep(_retry_delay(attempt))
                continue
            if response.status_code in RETRY_STATUS_CODES and attempt < self.retries:
                retry_after = _parse_retry_after(response)
                if retry_after is not None and retry_after > MAX_RETRY_DELAY:
                    return response
                await close_response(response)
                await asyncio.sleep(_retry_delay(attempt, retry_after))
                continue
            return response
        raise AssertionError("unreachable")

    async def aclose(self) -> None:
        if not self.closed:
            self.closed = True
            if self._owns_client and self._client is not None:
                await self._client.aclose()


async def close_response(response: Any) -> None:
    """소비한 비동기 응답을 닫습니다."""
    close = getattr(response, "aclose", None)
    if callable(close):
        await close()


def resolve_transport(
    transport: Any,
    session: Any,
    *,
    retries: int,
    timeout: float,
    max_rps: float,
    rate_limiter: AsyncTokenBucket | None,
) -> AsyncHttpxTransport:
    """주입한 세션은 호출자가 소유하며 transport는 송신 예산을 유지합니다."""
    if transport is not None and session is not None:
        raise ValueError("pass only one of transport or session")
    provided = transport if transport is not None else session
    if isinstance(provided, AsyncHttpxTransport):
        if rate_limiter is not None and rate_limiter is not provided.rate_limiter:
            raise ValueError("configure the injected transport with the same rate_limiter")
        return provided
    return AsyncHttpxTransport(
        timeout=timeout,
        retries=retries,
        max_rps=max_rps,
        rate_limiter=rate_limiter,
        client=provided,
    )
