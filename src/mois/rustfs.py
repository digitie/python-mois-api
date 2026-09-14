"""RustFS/S3 호환 오브젝트 스토리지 연동을 위한 경량 클라이언트 및 설정."""

from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, cast
from urllib.parse import quote, urlsplit

import httpx

from ._file_io import run_file_io
from ._ratelimit import AsyncTokenBucket

_EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
_SERVICE = "s3"
_AWS4_REQUEST = "aws4_request"


def normalize_object_prefix(value: str) -> str:
    """오브젝트 키 접두사를 정규화합니다."""
    normalized = value.replace("\\", "/").strip("/")
    parts = [
        part
        for part in PurePosixPath(normalized).parts
        if part not in {"", ".", "..", "/"} and ":" not in part
    ]
    return str(PurePosixPath(*parts)) if parts else "python-mois-api"


def join_object_key(*parts: str | Path) -> str:
    """오브젝트 경로 파트들을 합쳐서 정규화된 키를 만듭니다."""
    joined: list[str] = []
    for part in parts:
        text = str(part).replace("\\", "/").strip("/")
        if not text:
            continue
        joined.append(normalize_object_prefix(text))
    return str(PurePosixPath(*joined)) if joined else "python-mois-api"


def _sha256_file(path: Path) -> str:
    """파일의 SHA256 해시를 동기식으로 계산합니다."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


async def sha256_file(path: Path) -> str:
    """파일의 SHA256 해시를 비동기식으로 계산합니다."""
    return await run_file_io(_sha256_file, path)


class AsyncFileChunkIterator:
    """비동기 파일 청크 스트리밍 이터레이터."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._f: Any = None

    def __aiter__(self) -> AsyncFileChunkIterator:
        return self

    async def __anext__(self) -> bytes:
        if self._f is None:
            self._f = self.path.open("rb")
        chunk = await run_file_io(self._f.read, 1024 * 1024)
        if not chunk:
            await self.aclose()
            raise StopAsyncIteration
        return cast(bytes, chunk)

    async def aclose(self) -> None:
        if self._f is not None:
            await run_file_io(self._f.close)
            self._f = None


@dataclass(frozen=True)
class EffectiveRustfsConfig:
    """런타임에서 유효한 RustFS 연동 설정."""

    enabled: bool
    endpoint_url: str
    bucket: str
    prefix: str
    region: str
    force_path_style: bool
    access_key: str | None = field(repr=False)
    secret_key: str | None = field(repr=False)

    @classmethod
    def from_env(cls) -> EffectiveRustfsConfig:
        """환경 변수로부터 RustFS 설정을 로드합니다."""
        enabled_str = os.getenv("MOIS_RUSTFS_ENABLED", "false").lower()
        enabled = enabled_str in ("true", "1", "yes")
        endpoint_url = os.getenv("MOIS_RUSTFS_ENDPOINT_URL", "http://127.0.0.1:9003")
        bucket = os.getenv("MOIS_RUSTFS_BUCKET", "mois-data")
        prefix = os.getenv("MOIS_RUSTFS_PREFIX", "python-mois-api")
        region = os.getenv("MOIS_RUSTFS_REGION", "us-east-1")
        force_path_style_str = os.getenv("MOIS_RUSTFS_FORCE_PATH_STYLE", "true").lower()
        force_path_style = force_path_style_str in ("true", "1", "yes")
        access_key = os.getenv("MOIS_RUSTFS_ACCESS_KEY")
        secret_key = os.getenv("MOIS_RUSTFS_SECRET_KEY")

        return cls(
            enabled=enabled,
            endpoint_url=endpoint_url,
            bucket=bucket,
            prefix=normalize_object_prefix(prefix),
            region=region,
            force_path_style=force_path_style,
            access_key=access_key,
            secret_key=secret_key,
        )

    @property
    def credentials_configured(self) -> bool:
        """인증 정보가 올바르게 설정되었는지 여부를 반환합니다."""
        return bool(self.access_key and self.secret_key)

    def object_key(self, *parts: str | Path) -> str:
        """prefix를 포함한 오브젝트 키를 생성합니다."""
        return join_object_key(self.prefix, *parts)


def _canonical_header_value(value: str) -> str:
    return " ".join(value.split())


def canonical_query_string(query: dict[str, str]) -> str:
    pairs = []
    for key, value in sorted(query.items()):
        pairs.append(f"{quote(key, safe='-_.~')}={quote(value, safe='-_.~')}")
    return "&".join(pairs)


def _signing_key(secret_key: str, date_stamp: str, region: str) -> bytes:
    date_key = hmac.new(
        f"AWS4{secret_key}".encode(),
        date_stamp.encode(),
        hashlib.sha256,
    ).digest()
    region_key = hmac.new(date_key, region.encode(), hashlib.sha256).digest()
    service_key = hmac.new(region_key, _SERVICE.encode(), hashlib.sha256).digest()
    return hmac.new(service_key, _AWS4_REQUEST.encode(), hashlib.sha256).digest()


def _canonical_uri(*, bucket: str | None, key: str | None) -> str:
    parts: list[str] = []
    if bucket:
        parts.append(quote(bucket, safe="-_.~"))
    if key:
        parts.extend(quote(part, safe="-_.~") for part in key.split("/"))
    return "/" + "/".join(parts)


def _signed_request_helper(
    method: str,
    endpoint_url: str,
    parsed_endpoint: Any,
    bucket: str | None,
    key: str | None,
    query: dict[str, str] | None,
    headers: dict[str, str] | None,
    payload_hash: str,
    region: str,
    access_key: str | None = field(repr=False),
    secret_key: str | None = field(repr=False),
) -> tuple[str, dict[str, str]]:
    method = method.upper()
    request_time = datetime.now(UTC)
    amz_date = request_time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = request_time.strftime("%Y%m%d")
    canonical_uri = _canonical_uri(bucket=bucket, key=key)
    canonical_query = canonical_query_string(query or {})
    url = f"{endpoint_url}{canonical_uri}"
    if canonical_query:
        url = f"{url}?{canonical_query}"

    request_headers: dict[str, str] = {
        "host": parsed_endpoint.netloc,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }
    for name, value in (headers or {}).items():
        request_headers[name.lower()] = value.strip()

    canonical_headers = "".join(
        f"{name}:{_canonical_header_value(value)}\n"
        for name, value in sorted(request_headers.items())
    )
    signed_headers = ";".join(sorted(request_headers))
    canonical_request = "\n".join(
        [
            method,
            canonical_uri,
            canonical_query,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )
    credential_scope = f"{date_stamp}/{region}/{_SERVICE}/{_AWS4_REQUEST}"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    signing_key = _signing_key(secret_key or "", date_stamp, region)
    signature = hmac.new(
        signing_key,
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    request_headers["authorization"] = (
        "AWS4-HMAC-SHA256 "
        f"Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )
    return url, request_headers


def _strip_etag(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if stripped.startswith('"') and stripped.endswith('"'):
        return stripped[1:-1]
    return stripped or None


class RustfsClient:
    """RustFS 오브젝트 업로드를 위한 비동기식 SigV4 S3 클라이언트."""

    def __init__(
        self,
        config: EffectiveRustfsConfig,
        *,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        """비동기식 RustFS 클라이언트를 초기화합니다."""
        if not config.force_path_style:
            raise ValueError("RustFS path-style endpoint만 지원합니다")
        if not config.credentials_configured:
            raise ValueError("RustFS access key와 secret key가 설정되어 있지 않습니다")
        if session is not None and not isinstance(session, httpx.AsyncClient):
            raise TypeError("session must be httpx.AsyncClient")
        self.rate_limiter = rate_limiter if rate_limiter is not None else AsyncTokenBucket(max_rps)
        self._client = session
        self._owns_client = session is None
        self.closed = False
        self._config = config
        self._endpoint = config.endpoint_url.rstrip("/")
        self._parsed_endpoint = urlsplit(self._endpoint)
        if (
            self._parsed_endpoint.scheme not in {"http", "https"}
            or not self._parsed_endpoint.netloc
        ):
            raise ValueError(f"invalid RustFS endpoint_url: {config.endpoint_url}")

    async def __aenter__(self) -> RustfsClient:
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if not self.closed:
            self.closed = True
            if self._owns_client and self._client is not None:
                await self._client.aclose()

    async def ensure_bucket(self) -> None:
        """비동기식으로 버킷의 존재를 확인하고 없으면 새로 생성합니다."""
        head = await self._request(
            "HEAD",
            bucket=self._config.bucket,
            expected_status=(200, 404),
        )
        if head.status_code == 200:
            return
        put = await self._request(
            "PUT",
            bucket=self._config.bucket,
            expected_status=(200, 201, 204, 409),
        )
        if put.status_code == 409 and "BucketAlready" not in put.text:
            raise ValueError(f"RustFS bucket creation failed: HTTP {put.status_code}")

    async def put_file(
        self,
        key: str,
        path: Path,
        *,
        sha256: str | None = None,
    ) -> str | None:
        """비동기식으로 로컬 파일을 RustFS 스토리지에 업로드합니다."""
        await self.ensure_bucket()
        digest = sha256 or await sha256_file(path)
        stat = await run_file_io(path.stat)
        headers = {
            "content-length": str(stat.st_size),
            "content-type": "application/octet-stream",
            "x-amz-content-sha256": digest,
        }
        response = await self._request(
            "PUT",
            bucket=self._config.bucket,
            key=key,
            headers=headers,
            content=AsyncFileChunkIterator(path),
            payload_hash=digest,
            expected_status=(200, 201, 204),
        )
        return _strip_etag(response.headers.get("etag"))

    async def _request(
        self,
        method: str,
        *,
        bucket: str | None = None,
        key: str | None = None,
        query: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        content: Any = None,
        payload_hash: str = _EMPTY_SHA256,
        expected_status: tuple[int, ...],
    ) -> httpx.Response:
        if self.closed:
            raise RuntimeError("client is closed")
        if self._client is not None and self._client.auth is not None:
            raise TypeError("RustFS uses signed headers; session auth is unsupported")
        await self.rate_limiter.acquire()
        if self.closed:
            raise RuntimeError("client is closed")
        if self._client is not None and self._client.auth is not None:
            raise TypeError("RustFS uses signed headers; session auth is unsupported")
        url, signed_headers = _signed_request_helper(
            method,
            endpoint_url=self._endpoint,
            parsed_endpoint=self._parsed_endpoint,
            bucket=bucket,
            key=key,
            query=query,
            headers=headers,
            payload_hash=payload_hash,
            region=self._config.region,
            access_key=self._config.access_key,
            secret_key=self._config.secret_key,
        )
        timeout = httpx.Timeout(60.0, connect=10.0, read=None, write=None, pool=10.0)
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=timeout)
        try:
            response = await self._client.request(
                method, url, headers=signed_headers, content=content, follow_redirects=False
            )
        finally:
            if isinstance(content, AsyncFileChunkIterator):
                await content.aclose()
        if response.status_code not in expected_status:
            raise ValueError(f"RustFS request failed: HTTP {response.status_code}")
        return response
