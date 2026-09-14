"""data.go.kr 지방행정 인허가정보 OpenAPI 클라이언트."""

from __future__ import annotations

import inspect
import os
from collections.abc import AsyncIterator, Iterable, Mapping
from datetime import date, datetime
from types import TracebackType
from typing import Any

from ._http import (
    HTTP_CLIENT_ERROR,
    AsyncHttpxTransport,
    raise_for_http_error,
    resolve_transport,
)
from ._ratelimit import AsyncTokenBucket
from .catalogs import get_openapi_service
from .convert import KST
from .debug import DebugRun, error_to_dict, jsonable, redact_secret, redact_sensitive
from .exceptions import MoisCatalogError, MoisError, MoisRequestError
from .models import Condition, ConditionOperator, MoisResponse, OpenApiKind
from .parser import parse_openapi_response
from .processor import process_openapi_response


class MoisClient:
    """공공데이터포털 인허가정보 OpenAPI asyncio 클라이언트."""

    def __init__(
        self,
        service_key: str | None = None,
        *,
        api_key: str | None = None,
        timeout: float = 10.0,
        retries: int = 2,
        max_rps: float = 5.0,
        rate_limiter: AsyncTokenBucket | None = None,
        session: Any | None = None,
        transport: Any | None = None,
        base_url: str | None = None,
    ) -> None:
        resolved_key = _resolve_service_key(service_key, api_key)
        if not resolved_key:
            raise MoisRequestError("service_key is required")
        self.service_key = resolved_key
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
        self.session = self.transport
        self.base_url = base_url.rstrip("/") if base_url else None
        self.closed = False

    @classmethod
    def from_env(
        cls,
        name: str = "DATA_GO_KR_SERVICE_KEY",
        **kwargs: Any,
    ) -> MoisClient:
        """환경변수에서 서비스키를 읽어 비동기 클라이언트를 만듭니다."""

        try:
            service_key = os.environ[name]
        except KeyError as exc:
            raise MoisRequestError(f"{name} is not set") from exc
        return cls(service_key, **kwargs)

    async def __aenter__(self) -> MoisClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """소유한 async HTTP transport를 닫습니다."""

        aclose = getattr(self.transport, "aclose", None)
        if not self.closed and self._owns_transport and callable(aclose):
            await aclose()
        self.closed = True

    async def request(
        self,
        slug: str,
        *,
        kind: str | OpenApiKind = OpenApiKind.INFO,
        page_no: int = 1,
        num_of_rows: int = 100,
        conditions: Mapping[str, Any] | Iterable[Condition] | None = None,
        params: Mapping[str, Any] | None = None,
        org_code: str | None = None,
    ) -> MoisResponse:
        """업종 slug와 구분(info/history)으로 한 페이지를 비동기로 호출합니다.

        `org_code`는 개방자치단체코드(opnSfTeamCode) 7자리입니다.
        예: 서울 3610000, 부산 3620000, 경기 3710000.
        """

        url, request_params, kind_value = _build_openapi_request(
            self.service_key,
            self.base_url,
            slug,
            kind=kind,
            page_no=page_no,
            num_of_rows=num_of_rows,
            conditions=conditions,
            params=params,
            org_code=org_code,
        )
        response = await self._send_openapi_request(
            url,
            request_params,
            context=f"{slug}/{kind_value}",
        )
        try:
            return parse_openapi_response(response, page_no=page_no, num_of_rows=num_of_rows)
        except MoisError as exc:
            exc.args = tuple(
                _mask_request(value, self.service_key, request_params) for value in exc.args
            )
            exc.result_code = _mask_request(exc.result_code, self.service_key, request_params)
            raise exc from None

    async def debug_request(
        self,
        slug: str,
        *,
        kind: str | OpenApiKind = OpenApiKind.INFO,
        page_no: int = 1,
        num_of_rows: int = 100,
        conditions: Mapping[str, Any] | Iterable[Condition] | None = None,
        params: Mapping[str, Any] | None = None,
        org_code: str | None = None,
    ) -> DebugRun:
        """OpenAPI 1회 비동기 실행의 요청/응답/파싱/가공 결과를 반환합니다."""

        request_params: dict[str, Any] = {}
        trace: list[str] = []
        request_data: dict[str, Any] = {}
        response_data: dict[str, Any] = {}
        parsed: MoisResponse | None = None
        processed: list[Mapping[str, Any]] | None = None
        error: dict[str, Any] | None = None
        input_data: dict[str, Any] = {
            "slug": slug,
            "kind": str(kind),
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "params": dict(params or {}),
        }

        try:
            url, request_params, kind_value = _build_openapi_request(
                self.service_key,
                self.base_url,
                slug,
                kind=kind,
                page_no=page_no,
                num_of_rows=num_of_rows,
                conditions=conditions,
                params=params,
                org_code=org_code,
            )
            input_data["conditions"] = {
                key: value for key, value in request_params.items() if key.startswith("cond[")
            }
            request_data = {
                "method": "GET",
                "url": url,
                "query": request_params,
                "headers": {"Accept": "*/*"},
            }
            trace.append("OpenAPI 요청을 구성했습니다.")

            response = await self._send_openapi_request(
                url,
                request_params,
                context=f"{slug}/{kind_value}",
            )
            request_data["headers"] = _actual_request_headers(response, request_data["headers"])
            response_data = _response_debug_data(response)
            trace.append("OpenAPI 응답을 받았습니다.")

            parsed = parse_openapi_response(response, page_no=page_no, num_of_rows=num_of_rows)
            trace.append("원본 응답을 MoisResponse로 파싱했습니다.")

            processed = process_openapi_response(parsed)
            trace.append("파싱 결과를 라이브러리 반환 형태로 가공했습니다.")
        except Exception as exc:
            error = _redact_error_secret(error_to_dict(exc), self.service_key)
            trace.append("실행 중 예외를 캡처했습니다.")

        return DebugRun(
            function="openapi_request",
            input=_mask_request(
                redact_sensitive(jsonable(input_data)), self.service_key, request_params
            ),
            request=_mask_request(
                redact_sensitive(jsonable(request_data)), self.service_key, request_params
            ),
            response=_mask_request(
                redact_sensitive(jsonable(response_data)), self.service_key, request_params
            ),
            parsed=_mask_request(parsed, self.service_key, request_params),
            processed=_mask_request(processed, self.service_key, request_params),
            trace=tuple(trace),
            error=_mask_request(
                redact_sensitive(jsonable(error)), self.service_key, request_params
            ),
        )

    async def get(
        self,
        slug: str,
        *,
        kind: str | OpenApiKind = OpenApiKind.INFO,
        page_no: int = 1,
        num_of_rows: int = 100,
        conditions: Mapping[str, Any] | Iterable[Condition] | None = None,
        params: Mapping[str, Any] | None = None,
        org_code: str | None = None,
    ) -> list[Mapping[str, Any]]:
        """한 페이지의 item 목록만 비동기로 반환합니다."""

        return process_openapi_response(
            await self.request(
                slug,
                kind=kind,
                page_no=page_no,
                num_of_rows=num_of_rows,
                conditions=conditions,
                params=params,
                org_code=org_code,
            )
        )

    async def iter_records(
        self,
        slug: str,
        *,
        kind: str | OpenApiKind = OpenApiKind.INFO,
        num_of_rows: int = 100,
        conditions: Mapping[str, Any] | Iterable[Condition] | None = None,
        params: Mapping[str, Any] | None = None,
        max_pages: int | None = None,
        org_code: str | None = None,
    ) -> AsyncIterator[Mapping[str, Any]]:
        """페이지를 넘기며 모든 item을 비동기로 순회합니다."""

        page_no = 1
        seen = 0
        previous_items: tuple[Mapping[str, Any], ...] | None = None
        while True:
            response = await self.request(
                slug,
                kind=kind,
                page_no=page_no,
                num_of_rows=num_of_rows,
                conditions=conditions,
                params=params,
                org_code=org_code,
            )
            if not response.items:
                return
            if previous_items is not None and response.items == previous_items:
                return
            for item in response.items:
                seen += 1
                yield item
            if response.total_count is not None and seen >= response.total_count:
                return
            previous_items = response.items
            page_no += 1
            if max_pages is not None and page_no > max_pages:
                return

    async def iter_updated(
        self,
        slug: str,
        since: date | datetime | str,
        *,
        source_modified: bool = False,
        num_of_rows: int = 100,
        params: Mapping[str, Any] | None = None,
        max_pages: int | None = None,
        org_code: str | None = None,
    ) -> AsyncIterator[Mapping[str, Any]]:
        """증분 변경분을 비동기로 순회합니다."""

        field = "LAST_MDFCN_PNT" if source_modified else "DAT_UPDT_PNT"
        async for item in self.iter_records(
            slug,
            num_of_rows=num_of_rows,
            conditions=[Condition(field, ConditionOperator.GTE, _timestamp_param(since))],
            params=params,
            max_pages=max_pages,
            org_code=org_code,
        ):
            yield item

    async def get_updated(
        self,
        slug: str,
        since: date | datetime | str,
        *,
        source_modified: bool = False,
        num_of_rows: int = 100,
        params: Mapping[str, Any] | None = None,
        max_pages: int | None = None,
        org_code: str | None = None,
    ) -> list[Mapping[str, Any]]:
        """증분 변경분을 비동기 목록으로 반환합니다."""

        return [
            item
            async for item in self.iter_updated(
                slug,
                since,
                source_modified=source_modified,
                num_of_rows=num_of_rows,
                params=params,
                max_pages=max_pages,
                org_code=org_code,
            )
        ]

    async def iter_history_at(
        self,
        slug: str,
        base_date: date | str,
        *,
        org_code: str | None = None,
        num_of_rows: int = 100,
        params: Mapping[str, Any] | None = None,
        max_pages: int | None = None,
    ) -> AsyncIterator[Mapping[str, Any]]:
        """특정 기준일자의 이력 데이터를 비동기로 순회합니다."""

        conditions: list[Condition] = [
            Condition("BASE_DATE", ConditionOperator.EQ, _date_param(base_date))
        ]
        if org_code:
            conditions.append(Condition("OPN_ATMY_GRP_CD", ConditionOperator.EQ, org_code))
        async for item in self.iter_records(
            slug,
            kind="history",
            num_of_rows=num_of_rows,
            conditions=conditions,
            params=params,
            max_pages=max_pages,
        ):
            yield item

    async def get_history_at(
        self,
        slug: str,
        base_date: date | str,
        *,
        org_code: str | None = None,
        num_of_rows: int = 100,
        params: Mapping[str, Any] | None = None,
        max_pages: int | None = None,
    ) -> list[Mapping[str, Any]]:
        """특정 기준일자의 이력 데이터를 비동기 목록으로 반환합니다."""

        return [
            item
            async for item in self.iter_history_at(
                slug,
                base_date,
                org_code=org_code,
                num_of_rows=num_of_rows,
                params=params,
                max_pages=max_pages,
            )
        ]

    def __getattr__(self, name: str) -> Any:
        """`await client.get_hospitals()` 같은 비동기 편의 메서드를 제공합니다."""

        if name.startswith("get_updated_"):
            slug = name[len("get_updated_") :]
            _require_known_slug(slug, name)

            async def updated_getter(
                since: date | datetime | str,
                **kwargs: Any,
            ) -> list[Mapping[str, Any]]:
                return await self.get_updated(slug, since, **kwargs)

            return updated_getter
        if name.startswith("iter_updated_"):
            slug = name[len("iter_updated_") :]
            _require_known_slug(slug, name)

            async def updated_iterator(
                since: date | datetime | str,
                **kwargs: Any,
            ) -> AsyncIterator[Mapping[str, Any]]:
                async for item in self.iter_updated(slug, since, **kwargs):
                    yield item

            return updated_iterator

        if name.startswith("get_"):
            slug, kind = _dynamic_name_to_slug(name[4:])
            _require_known_slug(slug, name)

            async def getter(**kwargs: Any) -> list[Mapping[str, Any]]:
                return await self.get(slug, kind=kind, **kwargs)

            return getter
        if name.startswith("iter_"):
            slug, kind = _dynamic_name_to_slug(name[5:])
            _require_known_slug(slug, name)

            async def iterator(**kwargs: Any) -> AsyncIterator[Mapping[str, Any]]:
                async for item in self.iter_records(slug, kind=kind, **kwargs):
                    yield item

            return iterator
        raise AttributeError(name)

    async def _send_openapi_request(
        self,
        url: str,
        request_params: Mapping[str, Any],
        *,
        context: str,
    ) -> Any:
        if self.closed:
            raise RuntimeError("client is closed")
        try:
            result = self.transport.get(url, params=dict(request_params), timeout=self.timeout)
            if not inspect.isawaitable(result):
                raise TypeError("session.get must be async")
            response = await result
            raise_for_http_error(response, context)
        except HTTP_CLIENT_ERROR:
            raise MoisRequestError(f"{context}: request failed") from None
        return response


def _resolve_service_key(service_key: str | None, api_key: str | None) -> str | None:
    """service_key가 api_key보다 우선하며, 서로 다른 값이 함께 오면 오류입니다."""

    if service_key is not None and api_key is not None and service_key != api_key:
        raise MoisRequestError("service_key와 api_key에 서로 다른 값을 지정할 수 없습니다")
    resolved = service_key if service_key is not None else api_key
    if resolved is None:
        resolved = os.getenv("DATA_GO_KR_SERVICE_KEY")
    return resolved


def _require_known_slug(slug: str, name: str) -> None:
    try:
        get_openapi_service(slug)
    except MoisCatalogError as exc:
        raise AttributeError(name) from exc


def _actual_request_headers(response: Any, fallback: Mapping[str, str]) -> dict[str, Any]:
    try:
        headers = getattr(getattr(response, "request", None), "headers", None)
    except RuntimeError:
        headers = None
    if headers is None:
        return dict(fallback)
    return dict(headers)


def _redact_error_secret(error: dict[str, Any], secret: str | None) -> dict[str, Any]:
    if not secret:
        return error
    redacted = dict(error)
    message = redacted.get("message")
    if isinstance(message, str):
        redacted["message"] = message.replace(secret, "<REDACTED>")
    trace_lines = redacted.get("traceback")
    if isinstance(trace_lines, list):
        redacted["traceback"] = [
            line.replace(secret, "<REDACTED>") if isinstance(line, str) else line
            for line in trace_lines
        ]
    return redacted


def _endpoint_url(base_url: str | None, slug: str, kind: str) -> str:
    service = get_openapi_service(slug)
    if base_url:
        return f"{base_url}/{slug}/{kind}"
    return service.info_url if kind == "info" else service.history_url


def _build_openapi_request(
    service_key: str,
    base_url: str | None,
    slug: str,
    *,
    kind: str | OpenApiKind,
    page_no: int,
    num_of_rows: int,
    conditions: Mapping[str, Any] | Iterable[Condition] | None,
    params: Mapping[str, Any] | None,
    org_code: str | None = None,
) -> tuple[str, dict[str, Any], str]:
    kind_value = str(kind)
    if kind_value not in {OpenApiKind.INFO.value, OpenApiKind.HISTORY.value}:
        raise MoisRequestError('kind must be "info" or "history"')
    if page_no < 1:
        raise MoisRequestError("page_no must be >= 1")
    if not 1 <= num_of_rows <= 100:
        raise MoisRequestError("num_of_rows must be between 1 and 100")

    url = _endpoint_url(base_url, slug, kind_value)
    request_params: dict[str, Any] = {
        "serviceKey": service_key,
        "pageNo": page_no,
        "numOfRows": num_of_rows,
    }
    if org_code:
        request_params["opnSfTeamCode"] = org_code
    request_params.update(_condition_params(conditions))
    if params:
        request_params.update(params)
    return url, request_params, kind_value


def _response_debug_data(response: Any) -> dict[str, Any]:
    headers = dict(getattr(response, "headers", {}) or {})
    return {
        "status_code": getattr(response, "status_code", None),
        "headers": headers,
        "body": _response_debug_body(response, headers),
    }


def _response_debug_body(response: Any, headers: Mapping[str, Any]) -> Any:
    content_type = str(headers.get("Content-Type") or headers.get("content-type") or "").lower()
    text = getattr(response, "text", "")
    if "json" in content_type or str(text).lstrip().startswith("{"):
        try:
            return response.json()
        except (AttributeError, ValueError):
            return text
    return text


def _dynamic_name_to_slug(name: str) -> tuple[str, str]:
    if name.endswith("_history"):
        return name[: -len("_history")], "history"
    return name, "info"


def _condition_params(conditions: Mapping[str, Any] | Iterable[Condition] | None) -> dict[str, Any]:
    if conditions is None:
        return {}
    if isinstance(conditions, Mapping):
        params: dict[str, Any] = {}
        for field, value in conditions.items():
            if isinstance(value, tuple) and len(value) == 2:
                operator, actual_value = value
            else:
                operator, actual_value = ConditionOperator.EQ, value
            params[f"cond[{field}::{operator!s}]"] = actual_value
        return params
    return {condition.param_name(): condition.value for condition in conditions}


def _timestamp_param(value: date | datetime | str) -> str:
    """datetime/date/문자열을 KST 기준 YYYYMMDDHHMMSS로 변환합니다.

    tz-aware datetime은 KST로 변환하고, naive datetime은 이미 KST인 것으로 간주합니다.
    """

    if isinstance(value, datetime):
        if value.tzinfo is not None:
            value = value.astimezone(KST)
        return value.strftime("%Y%m%d%H%M%S")
    if isinstance(value, date):
        return value.strftime("%Y%m%d000000")
    text = str(value).strip()
    digits = "".join(char for char in text if char.isdigit())
    if len(digits) == 8:
        return f"{digits}000000"
    if len(digits) == 14:
        return digits
    raise MoisRequestError("since must be YYYYMMDD, YYYYMMDDHHMMSS, date, or datetime")


def _date_param(value: date | str) -> str:
    if isinstance(value, date):
        return value.strftime("%Y%m%d")
    text = str(value).strip()
    digits = "".join(char for char in text if char.isdigit())
    if len(digits) != 8:
        raise MoisRequestError("base_date must be YYYYMMDD or date")
    return digits


def _mask_request(obj: Any, configured_key: str, params: Mapping[str, Any]) -> Any:
    """클라이언트 기본 키와 params로 지정한 실제 송신 키를 모두 마스킹합니다."""
    obj = redact_secret(obj, configured_key)
    actual_key = params.get("serviceKey")
    if isinstance(actual_key, str) and actual_key:
        obj = redact_secret(obj, actual_key)
    return obj
