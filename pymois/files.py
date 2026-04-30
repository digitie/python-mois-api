"""file.localdata.go.kr 파일 다운로드와 CSV 로더."""

from __future__ import annotations

import csv
import io
import os
import zipfile
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from requests import RequestException

from ._http import build_session, raise_for_http_error
from .catalogs import get_file_download
from .convert import convert_value, field_for_header
from .coords import epsg5174_to_wgs84
from .exceptions import MoisParseError, MoisRequestError
from .models import Coordinate, LocalDataRecord

DEFAULT_FILE_BASE_URL = "https://file.localdata.go.kr"


class LocalDataFileClient:
    """localdata 인허가정보 CSV 파일 다운로드/로드 클라이언트."""

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        retries: int = 2,
        session: Any | None = None,
        base_url: str = DEFAULT_FILE_BASE_URL,
        validate_download_count: bool = True,
    ) -> None:
        self.timeout = timeout
        self.session = session or build_session(retries)
        self.base_url = base_url.rstrip("/")
        self.validate_download_count = validate_download_count

    def download_bytes(self, slug: str, *, org_code: str | None = None) -> bytes:
        """업종 slug의 전국 또는 지역 CSV 파일을 bytes로 다운로드합니다."""

        spec = get_file_download(slug)
        info_url = self._absolute(spec.info_path)
        download_url = self._absolute(spec.download_path)
        if org_code:
            download_url = f"{download_url}?{urlencode({'orgCode': org_code})}"

        try:
            self.session.get(
                info_url,
                headers={"Referer": self.base_url, "Accept": "text/html,application/xhtml+xml"},
                timeout=self.timeout,
            )
            if self.validate_download_count:
                validation = self.session.get(
                    self._absolute("/file/validate/download-count"),
                    headers={"Referer": info_url, "Accept": "*/*"},
                    timeout=self.timeout,
                )
                raise_for_http_error(validation, "localdata download validation")
            response = self.session.get(
                download_url,
                headers={"Referer": info_url, "Accept": "*/*"},
                timeout=self.timeout,
            )
            raise_for_http_error(response, f"localdata download {slug}")
        except RequestException as exc:
            raise MoisRequestError(f"localdata download failed: {slug}") from exc
        return bytes(response.content)

    def download(
        self,
        slug: str,
        output_path: str | os.PathLike[str],
        *,
        org_code: str | None = None,
    ) -> Path:
        """파일을 다운로드해서 `output_path`에 저장하고 경로를 반환합니다."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.download_bytes(slug, org_code=org_code))
        return path

    def load(
        self,
        slug: str,
        *,
        org_code: str | None = None,
        encoding: str | None = None,
    ) -> list[LocalDataRecord]:
        """업종 파일을 다운로드하고 `LocalDataRecord` 목록으로 로드합니다."""

        return load_records_from_bytes(
            self.download_bytes(slug, org_code=org_code),
            slug=slug,
            encoding=encoding,
        )

    def load_file(
        self,
        path: str | os.PathLike[str],
        *,
        slug: str | None = None,
        encoding: str | None = None,
    ) -> list[LocalDataRecord]:
        """이미 받은 CSV 파일을 `LocalDataRecord` 목록으로 로드합니다."""

        return load_records_from_bytes(Path(path).read_bytes(), slug=slug, encoding=encoding)

    def __getattr__(self, name: str) -> Any:
        """`load_hospitals()`, `download_hospitals()` 편의 메서드를 동적으로 제공합니다."""

        if name.startswith("load_"):
            slug = name[5:]

            def loader(**kwargs: Any) -> list[LocalDataRecord]:
                return self.load(slug, **kwargs)

            return loader
        if name.startswith("download_"):
            slug = name[len("download_") :]

            def downloader(output_path: str | os.PathLike[str], **kwargs: Any) -> Path:
                return self.download(slug, output_path, **kwargs)

            return downloader
        raise AttributeError(name)

    def _absolute(self, path_or_url: str) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        return f"{self.base_url}{path_or_url}"


def load_records_from_bytes(
    content: bytes,
    *,
    slug: str | None = None,
    encoding: str | None = None,
) -> list[LocalDataRecord]:
    """CSV bytes를 정규화된 객체 목록으로 변환합니다."""

    csv_bytes = _first_csv_bytes(content)
    text = _decode_csv(csv_bytes, encoding)
    return load_records_from_text(text, slug=slug)


def load_records_from_text(text: str, *, slug: str | None = None) -> list[LocalDataRecord]:
    """CSV 문자열을 정규화된 객체 목록으로 변환합니다."""

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise MoisParseError("CSV 헤더가 없습니다")
    spec = get_file_download(slug) if slug else None
    records: list[LocalDataRecord] = []
    for row in reader:
        raw = {str(key): value or "" for key, value in row.items() if key is not None}
        data: dict[str, Any] = {}
        for header, raw_value in raw.items():
            field = field_for_header(header)
            data[field] = convert_value(field, header, raw_value)
        coordinates = _coordinates_from_data(data)
        if coordinates is not None:
            data["WGS84_LON"] = coordinates.lon
            data["WGS84_LAT"] = coordinates.lat
        records.append(
            LocalDataRecord.build(
                service_slug=slug,
                category=spec.category if spec else None,
                title=spec.title if spec else None,
                data=data,
                raw=raw,
                coordinates=coordinates,
            )
        )
    return records


def _coordinates_from_data(data: dict[str, Any]) -> Coordinate | None:
    x = data.get("CRD_INFO_X")
    y = data.get("CRD_INFO_Y")
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return None
    lon, lat = epsg5174_to_wgs84(float(x), float(y))
    return Coordinate(x=float(x), y=float(y), lon=lon, lat=lat)


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
        return archive.read(candidates[0])


def _decode_csv(content: bytes, encoding: str | None) -> str:
    encodings: Iterable[str] = (encoding,) if encoding else ("utf-8-sig", "cp949", "euc-kr")
    last_error: UnicodeDecodeError | None = None
    for candidate in encodings:
        if candidate is None:
            continue
        try:
            return content.decode(candidate)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise MoisParseError("CSV 인코딩을 해석할 수 없습니다") from last_error
