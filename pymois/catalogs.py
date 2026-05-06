"""카탈로그 조회 도우미."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .catalog import (
    FILE_DOWNLOADS,
    INCREMENTAL_OPENAPI_ENDPOINTS,
    OPENAPI_ENDPOINTS,
    OPENAPI_SERVICES,
    RESPONSE_FIELDS,
)
from .exceptions import MoisCatalogError
from .models import (
    FileDownload,
    IncrementalOpenApiEndpoint,
    OpenApiEndpoint,
    OpenApiService,
    ResponseField,
)


def list_openapi_services(category: str | None = None) -> list[OpenApiService]:
    """구현 대상 OpenAPI 업종 195개 목록을 반환합니다."""

    rows = _filter_by_category(OPENAPI_SERVICES, category)
    return [_openapi_service(row) for row in rows]


def list_openapi_endpoints(
    *,
    kind: str | None = None,
    category: str | None = None,
) -> list[OpenApiEndpoint]:
    """OpenAPI 호출 URL 목록을 반환합니다.

    `kind`는 `"info"` 또는 `"history"`를 사용할 수 있습니다.
    """

    service_category = {row["slug"]: row["category"] for row in OPENAPI_SERVICES}
    rows: Iterable[dict[str, Any]] = OPENAPI_ENDPOINTS
    if kind is not None:
        rows = [row for row in rows if row["kind"] == kind]
    if category is not None:
        rows = [row for row in rows if service_category.get(row["service_slug"]) == category]
    return [_openapi_endpoint(row) for row in rows]


def get_openapi_service(slug: str) -> OpenApiService:
    """slug로 OpenAPI 업종 명세를 찾습니다."""

    for row in OPENAPI_SERVICES:
        if row["slug"] == slug:
            return _openapi_service(row)
    raise MoisCatalogError(f"알 수 없는 OpenAPI slug입니다: {slug}")


def list_incremental_openapi_endpoints(
    category: str | None = None,
) -> list[IncrementalOpenApiEndpoint]:
    """증분조회 가능한 OpenAPI 195개 목록을 반환합니다."""

    rows = _filter_by_category(INCREMENTAL_OPENAPI_ENDPOINTS, category)
    return [_incremental_openapi_endpoint(row) for row in rows]


def get_incremental_openapi_endpoint(slug: str) -> IncrementalOpenApiEndpoint:
    """slug로 증분조회 OpenAPI 명세를 찾습니다."""

    for row in INCREMENTAL_OPENAPI_ENDPOINTS:
        if row["service_slug"] == slug:
            return _incremental_openapi_endpoint(row)
    raise MoisCatalogError(f"알 수 없는 증분 OpenAPI slug입니다: {slug}")


def list_file_downloads(
    *,
    kind: str | None = "license",
    category: str | None = None,
) -> list[FileDownload]:
    """localdata 파일 다운로드 목록을 반환합니다.

    기본값은 인허가정보 195개만 반환합니다. 생활편의정보까지 보려면
    `kind=None` 또는 `kind="life_convenience"`를 사용합니다.
    """

    rows: Iterable[dict[str, Any]] = FILE_DOWNLOADS
    if kind is not None:
        rows = [row for row in rows if row["kind"] == kind]
    if category is not None:
        rows = [row for row in rows if row["category"] == category]
    return [_file_download(row) for row in rows]


def get_file_download(slug: str) -> FileDownload:
    """slug로 localdata 파일 다운로드 명세를 찾습니다."""

    for row in FILE_DOWNLOADS:
        if row["slug"] == slug:
            return _file_download(row)
    raise MoisCatalogError(f"알 수 없는 파일 다운로드 slug입니다: {slug}")


def list_response_fields(
    *,
    group: str | None = None,
    include_deleted: bool = False,
) -> list[ResponseField]:
    """붙임3의 응답변수 매핑 목록을 반환합니다."""

    rows: Iterable[dict[str, Any]] = RESPONSE_FIELDS
    if group is not None:
        rows = [row for row in rows if row["group"] == group]
    if not include_deleted:
        rows = [row for row in rows if not row["deleted"]]
    return [_response_field(row) for row in rows]


def get_response_field(field: str) -> ResponseField:
    """공공데이터포털 응답변수명으로 필드 명세를 찾습니다."""

    for row in RESPONSE_FIELDS:
        if row["field"] == field:
            return _response_field(row)
    raise MoisCatalogError(f"알 수 없는 응답변수입니다: {field}")


def _filter_by_category(
    rows: Iterable[dict[str, Any]],
    category: str | None,
) -> Iterable[dict[str, Any]]:
    if category is None:
        return rows
    return [row for row in rows if row["category"] == category]


def _text(row: Mapping[str, Any], key: str) -> str:
    return str(row[key])


def _optional_text(row: Mapping[str, Any], key: str) -> str | None:
    value = row.get(key)
    return str(value) if value is not None else None


def _openapi_service(row: Mapping[str, Any]) -> OpenApiService:
    return OpenApiService(
        index=int(row["index"]),
        slug=_text(row, "slug"),
        category=_text(row, "category"),
        name=_text(row, "name"),
        title=_text(row, "title"),
        service_name=_text(row, "service_name"),
        application_url=_text(row, "application_url"),
        info_url=_text(row, "info_url"),
        history_url=_text(row, "history_url"),
        info_operation=_text(row, "info_operation"),
        history_operation=_text(row, "history_operation"),
    )


def _openapi_endpoint(row: Mapping[str, Any]) -> OpenApiEndpoint:
    return OpenApiEndpoint(
        service_slug=_text(row, "service_slug"),
        kind=_text(row, "kind"),
        operation_name=_text(row, "operation_name"),
        url=_text(row, "url"),
    )


def _incremental_openapi_endpoint(row: Mapping[str, Any]) -> IncrementalOpenApiEndpoint:
    return IncrementalOpenApiEndpoint(
        service_slug=_text(row, "service_slug"),
        category=_text(row, "category"),
        name=_text(row, "name"),
        title=_text(row, "title"),
        application_url=_text(row, "application_url"),
        info_url=_text(row, "info_url"),
        condition_field=_text(row, "condition_field"),
        source_modified_field=_text(row, "source_modified_field"),
        condition_operator=_text(row, "condition_operator"),
        get_method=_text(row, "get_method"),
        iter_method=_text(row, "iter_method"),
    )


def _file_download(row: Mapping[str, Any]) -> FileDownload:
    return FileDownload(
        slug=_text(row, "slug"),
        kind=_text(row, "kind"),
        category=_text(row, "category"),
        name=_text(row, "name"),
        title=_text(row, "title"),
        info_url=_text(row, "info_url"),
        download_url=_text(row, "download_url"),
        info_path=_text(row, "info_path"),
        download_path=_text(row, "download_path"),
    )


def _response_field(row: Mapping[str, Any]) -> ResponseField:
    length = row.get("length")
    return ResponseField(
        group=_optional_text(row, "group"),
        local_field=_optional_text(row, "local_field"),
        local_name=_optional_text(row, "local_name"),
        field=_optional_text(row, "field"),
        name=_optional_text(row, "name"),
        type=_optional_text(row, "type"),
        length=length if isinstance(length, (int, float, str)) else None,
        note=_optional_text(row, "note"),
        deleted=bool(row["deleted"]),
    )
