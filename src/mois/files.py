"""file.localdata.go.kr 파일 다운로드와 CSV 로더."""

from __future__ import annotations

import codecs
import csv
import io
import os
import tempfile
import zipfile
from collections.abc import AsyncIterator, Iterable, Iterator
from pathlib import Path
from typing import IO, Any, cast
from urllib.parse import urlencode

from pyproj.exceptions import ProjError

from ._file_io import run_file_io
from ._http import (
    HTTP_CLIENT_ERROR,
    AsyncHttpxTransport,
    close_response,
    raise_for_http_error,
    resolve_transport,
)
from ._ratelimit import AsyncTokenBucket
from .catalogs import get_file_download
from .convert import convert_value, field_for_header
from .exceptions import MoisParseError, MoisRequestError
from .models import Coordinate, LocalDataRecord
from .rustfs import EffectiveRustfsConfig, RustfsClient

DEFAULT_FILE_BASE_URL = "https://file.localdata.go.kr"
_ITERATION_DONE = object()
_MAX_ZIP_MEMBER_BYTES = 1024 * 1024 * 1024


class LocalDataFileClient:
    """localdata 인허가정보 CSV 파일 다운로드/로드 asyncio 클라이언트."""

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        retries: int = 2,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
        session: Any | None = None,
        transport: Any | None = None,
        base_url: str = DEFAULT_FILE_BASE_URL,
        validate_download_count: bool = True,
    ) -> None:
        self.timeout = timeout
        self.transport = resolve_transport(
            transport,
            session,
            retries=retries,
            timeout=timeout,
            max_rps=max_rps,
            rate_limiter=rate_limiter,
        )
        self.rate_limiter = self.transport.rate_limiter
        self._owns_transport = not isinstance(
            transport if transport is not None else session, AsyncHttpxTransport
        )
        self.closed = False
        self.session = self.transport
        self.base_url = base_url.rstrip("/")
        self.validate_download_count = validate_download_count

    async def __aenter__(self) -> LocalDataFileClient:
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """소유한 async HTTP transport를 닫습니다."""

        aclose = getattr(self.transport, "aclose", None)
        if not self.closed and self._owns_transport and callable(aclose):
            await aclose()
        self.closed = True

    async def download_bytes(self, slug: str, *, org_code: str | None = None) -> bytes:
        """업종 slug의 전국 또는 지역 CSV 파일을 bytes로 비동기 다운로드합니다."""

        with tempfile.TemporaryFile() as output:
            binary_output = cast(IO[bytes], output)
            await self._download_to_file(slug, binary_output, org_code=org_code)
            return await run_file_io(_read_all_bytes, binary_output)

    async def download(
        self,
        slug: str,
        output_path: str | os.PathLike[str],
        *,
        org_code: str | None = None,
    ) -> Path:
        """파일을 비동기로 다운로드해서 `output_path`에 저장하고 경로를 반환합니다."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as output:
            await self._download_to_file(slug, output, org_code=org_code)
        return path

    async def load(
        self,
        slug: str,
        *,
        org_code: str | None = None,
        encoding: str | None = None,
    ) -> list[LocalDataRecord]:
        """업종 파일을 비동기로 다운로드하고 `LocalDataRecord` 목록으로 로드합니다."""

        content = await self.download_bytes(slug, org_code=org_code)
        return await run_file_io(
            load_records_from_bytes,
            content,
            slug=slug,
            encoding=encoding,
        )

    async def iter(
        self,
        slug: str,
        *,
        org_code: str | None = None,
        encoding: str | None = None,
    ) -> AsyncIterator[LocalDataRecord]:
        """업종 파일을 비동기로 다운로드하고 `LocalDataRecord`를 한 행씩 순회합니다."""

        with tempfile.TemporaryFile() as output:
            binary_output = cast(IO[bytes], output)
            await self._download_to_file(slug, binary_output, org_code=org_code)
            binary_output.seek(0)
            records = iter_records_from_binary(binary_output, slug=slug, encoding=encoding)
            while True:
                record = await run_file_io(_next_record_or_done, records)
                if record is _ITERATION_DONE:
                    return
                yield cast(LocalDataRecord, record)

    async def load_file(
        self,
        path: str | os.PathLike[str],
        *,
        slug: str | None = None,
        encoding: str | None = None,
    ) -> list[LocalDataRecord]:
        """이미 받은 CSV 파일을 비동기로 `LocalDataRecord` 목록으로 로드합니다."""

        return await run_file_io(
            _load_records_from_path,
            path,
            slug=slug,
            encoding=encoding,
        )

    async def iter_file(
        self,
        path: str | os.PathLike[str],
        *,
        slug: str | None = None,
        encoding: str | None = None,
    ) -> AsyncIterator[LocalDataRecord]:
        """이미 받은 CSV 파일을 비동기로 한 행씩 순회합니다."""

        with Path(path).open("rb") as source:
            records = iter_records_from_binary(source, slug=slug, encoding=encoding)
            while True:
                record = await run_file_io(_next_record_or_done, records)
                if record is _ITERATION_DONE:
                    return
                yield cast(LocalDataRecord, record)

    async def download_to_rustfs(
        self,
        slug: str,
        output_path: str | os.PathLike[str],
        *,
        org_code: str | None = None,
        object_key: str | None = None,
        config: EffectiveRustfsConfig | None = None,
    ) -> str:
        """파일을 로컬 `output_path`에 비동기로 다운로드하고 동시에 RustFS에 저장(업로드)합니다."""
        await self.download(slug, output_path, org_code=org_code)

        cfg = config or EffectiveRustfsConfig.from_env()
        if not cfg.enabled:
            raise ValueError(
                "RustFS가 활성화되어 있지 않습니다. MOIS_RUSTFS_ENABLED=true 설정이 필요합니다."
            )

        filename = Path(output_path).name
        key = object_key or cfg.object_key(slug, filename)

        async with RustfsClient(cfg, rate_limiter=self.rate_limiter) as client:
            await client.put_file(key, Path(output_path))

        return f"rustfs://{cfg.bucket}/{key}"

    def __getattr__(self, name: str) -> Any:
        """`await files.load_hospitals()` 같은 비동기 편의 메서드를 제공합니다."""

        if name.startswith("download_") and name.endswith("_to_rustfs"):
            slug = name[len("download_") : -len("_to_rustfs")]

            async def downloader_to_rustfs(
                output_path: str | os.PathLike[str], **kwargs: Any
            ) -> str:
                return await self.download_to_rustfs(slug, output_path, **kwargs)

            return downloader_to_rustfs

        if name.startswith("iter_"):
            slug = name[len("iter_") :]

            async def iterator(**kwargs: Any) -> AsyncIterator[LocalDataRecord]:
                async for record in self.iter(slug, **kwargs):
                    yield record

            return iterator
        if name.startswith("load_"):
            slug = name[5:]

            async def loader(**kwargs: Any) -> list[LocalDataRecord]:
                return await self.load(slug, **kwargs)

            return loader
        if name.startswith("download_"):
            slug = name[len("download_") :]

            async def downloader(output_path: str | os.PathLike[str], **kwargs: Any) -> Path:
                return await self.download(slug, output_path, **kwargs)

            return downloader
        raise AttributeError(name)

    def _absolute(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return f"{self.base_url}{path_or_url}"

    async def _download_to_file(
        self,
        slug: str,
        output: IO[bytes],
        *,
        org_code: str | None = None,
    ) -> None:
        if self.closed:
            raise RuntimeError("client is closed")
        spec = get_file_download(slug)
        info_url = self._absolute(spec.info_path)
        download_url = self._absolute(spec.download_path)
        if org_code:
            download_url = f"{download_url}?{urlencode({'orgCode': org_code})}"

        response: Any | None = None
        try:
            landing = await self.transport.get(
                info_url,
                headers={"Referer": self.base_url, "Accept": "text/html,application/xhtml+xml"},
                timeout=self.timeout,
            )
            try:
                raise_for_http_error(landing, "localdata landing")
            finally:
                await close_response(landing)
            if self.validate_download_count:
                validation = await self.transport.get(
                    self._absolute("/file/validate/download-count"),
                    headers={"Referer": info_url, "Accept": "*/*"},
                    timeout=self.timeout,
                )
                try:
                    raise_for_http_error(validation, "localdata download validation")
                finally:
                    await close_response(validation)
            response = await self.transport.get(
                download_url,
                headers={"Referer": info_url, "Accept": "*/*"},
                timeout=self.timeout,
                stream=True,
            )
            raise_for_http_error(response, f"localdata download {slug}")
            await _write_response_to_file_async(response, output)
        except HTTP_CLIENT_ERROR as exc:
            raise MoisRequestError(f"localdata download failed: {slug}") from exc
        finally:
            await close_response(response)


def load_records_from_bytes(
    content: bytes,
    *,
    slug: str | None = None,
    encoding: str | None = None,
) -> list[LocalDataRecord]:
    """CSV bytes를 정규화된 객체 목록으로 변환합니다."""

    return list(iter_records_from_bytes(content, slug=slug, encoding=encoding))


def _load_records_from_path(
    path: str | os.PathLike[str],
    *,
    slug: str | None = None,
    encoding: str | None = None,
) -> list[LocalDataRecord]:
    with Path(path).open("rb") as source:
        return list(iter_records_from_binary(source, slug=slug, encoding=encoding))


def _next_record_or_done(records: Iterator[LocalDataRecord]) -> LocalDataRecord | object:
    try:
        return next(records)
    except StopIteration:
        return _ITERATION_DONE


def _read_all_bytes(stream: IO[bytes]) -> bytes:
    stream.seek(0)
    return stream.read()


def iter_records_from_bytes(
    content: bytes,
    *,
    slug: str | None = None,
    encoding: str | None = None,
) -> Iterator[LocalDataRecord]:
    """CSV bytes를 정규화된 객체로 한 행씩 변환합니다."""

    csv_bytes = _first_csv_bytes(content)
    selected_encoding = _choose_csv_encoding(csv_bytes, encoding)
    stream = io.TextIOWrapper(io.BytesIO(csv_bytes), encoding=selected_encoding)
    try:
        yield from _iter_records_from_reader(csv.DictReader(stream), slug=slug)
    except UnicodeDecodeError as exc:
        raise MoisParseError("CSV 인코딩을 해석할 수 없습니다") from exc


def iter_records_from_binary(
    source: IO[bytes],
    *,
    slug: str | None = None,
    encoding: str | None = None,
) -> Iterator[LocalDataRecord]:
    """seek 가능한 binary CSV/ZIP 스트림을 정규화된 객체로 순회합니다."""

    if _is_zip_binary(source):
        with zipfile.ZipFile(source) as archive:
            candidates = [
                name
                for name in archive.namelist()
                if not name.endswith("/") and name.lower().endswith((".csv", ".txt"))
            ]
            if not candidates:
                raise MoisParseError("ZIP 파일 안에서 CSV를 찾을 수 없습니다")
            with archive.open(candidates[0]) as csv_file:
                selected_encoding = _peek_csv_encoding(csv_file, encoding)
                yield from _iter_records_from_binary_reader(
                    csv_file,
                    slug=slug,
                    encoding=selected_encoding,
                )
        return

    source.seek(0)
    selected_encoding = _peek_csv_encoding(source, encoding)
    yield from _iter_records_from_binary_reader(source, slug=slug, encoding=selected_encoding)


def load_records_from_text(text: str, *, slug: str | None = None) -> list[LocalDataRecord]:
    """CSV 문자열을 정규화된 객체 목록으로 변환합니다."""

    return list(iter_records_from_text(text, slug=slug))


def iter_records_from_text(text: str, *, slug: str | None = None) -> Iterator[LocalDataRecord]:
    """CSV 문자열을 정규화된 객체로 한 행씩 변환합니다."""

    yield from _iter_records_from_reader(csv.DictReader(io.StringIO(text)), slug=slug)


def _iter_records_from_reader(
    reader: csv.DictReader[str],
    *,
    slug: str | None = None,
) -> Iterator[LocalDataRecord]:
    if not reader.fieldnames:
        raise MoisParseError("CSV 헤더가 없습니다")
    spec = get_file_download(slug) if slug else None
    for row in reader:
        raw = {str(key): value or "" for key, value in row.items() if key is not None}
        data: dict[str, Any] = {}
        for header, raw_value in raw.items():
            field = field_for_header(header)
            data[field] = convert_value(field, header, raw_value)
        try:
            coordinates = _coordinates_from_data(data)
        except (ValueError, ProjError):
            coordinates = None
        if coordinates is not None:
            data["WGS84_LON"] = coordinates.lon
            data["WGS84_LAT"] = coordinates.lat
        yield LocalDataRecord.build(
            service_slug=slug,
            category=spec.category if spec else None,
            title=spec.title if spec else None,
            data=data,
            raw=raw,
            coordinates=coordinates,
        )


def _iter_records_from_binary_reader(
    source: IO[bytes],
    *,
    slug: str | None = None,
    encoding: str,
) -> Iterator[LocalDataRecord]:
    stream = io.TextIOWrapper(source, encoding=encoding, newline="")
    try:
        yield from _iter_records_from_reader(csv.DictReader(stream), slug=slug)
    except UnicodeDecodeError as exc:
        raise MoisParseError("CSV 인코딩을 해석할 수 없습니다") from exc


def _coordinates_from_data(data: dict[str, Any]) -> Coordinate | None:
    x = data.get("CRD_INFO_X")
    y = data.get("CRD_INFO_Y")
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return None
    return Coordinate.from_katec(float(x), float(y))


def _first_csv_bytes(content: bytes) -> bytes:
    if not zipfile.is_zipfile(io.BytesIO(content)):
        return content
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        candidates = [
            name
            for name in archive.namelist()
            if not name.endswith("/") and name.lower().endswith((".csv", ".txt"))
        ]
        if not candidates:
            raise MoisParseError("ZIP 파일 안에서 CSV를 찾을 수 없습니다")
        info = archive.getinfo(candidates[0])
        if info.file_size > _MAX_ZIP_MEMBER_BYTES:
            raise MoisParseError("ZIP 안의 CSV가 허용된 최대 크기를 초과합니다")
        return archive.read(candidates[0])


def _is_zip_binary(source: IO[bytes]) -> bool:
    position = source.tell()
    try:
        return zipfile.is_zipfile(source)
    finally:
        source.seek(position)


async def _write_response_to_file_async(response: Any, output: IO[bytes]) -> None:
    aiter_bytes = getattr(response, "aiter_bytes", None)
    if callable(aiter_bytes):
        async for chunk in aiter_bytes(chunk_size=1024 * 1024):
            if chunk:
                await run_file_io(output.write, chunk)
        return
    await run_file_io(output.write, bytes(getattr(response, "content", b"")))


def _decode_csv(content: bytes, encoding: str | None) -> str:
    return content.decode(_choose_csv_encoding(content, encoding))


def _peek_csv_encoding(source: IO[bytes], encoding: str | None) -> str:
    if encoding:
        return encoding
    position = source.tell()
    try:
        sample = source.read(65536)
    finally:
        source.seek(position)
    return _choose_csv_encoding(sample, None, partial=True)


def _choose_csv_encoding(content: bytes, encoding: str | None, *, partial: bool = False) -> str:
    encodings: Iterable[str] = (encoding,) if encoding else ("utf-8-sig", "cp949", "euc-kr")
    last_error: UnicodeDecodeError | None = None
    for candidate in encodings:
        if candidate is None:
            continue
        try:
            _validate_decoding(content, candidate, final=not partial)
            return candidate
        except UnicodeDecodeError as exc:
            last_error = exc
    raise MoisParseError("CSV 인코딩을 해석할 수 없습니다") from last_error


def _validate_decoding(content: bytes, encoding: str, *, final: bool = True) -> None:
    decoder = codecs.getincrementaldecoder(encoding)()
    for offset in range(0, len(content), 65536):
        decoder.decode(content[offset : offset + 65536], final=False)
    decoder.decode(b"", final=final)
