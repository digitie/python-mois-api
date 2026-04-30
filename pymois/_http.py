"""HTTP 세션 생성과 공통 응답 처리."""

from __future__ import annotations

from typing import Any

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import MoisRequestError, MoisServerError

DEFAULT_USER_AGENT = "pymois/0.1 (+https://github.com/digitie/pymois)"


def build_session(retries: int = 2) -> Session:
    """재시도 정책이 적용된 requests 세션을 만듭니다."""

    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        status=retries,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def raise_for_http_error(response: Any, context: str) -> None:
    """HTTP 상태코드를 pymois 예외로 매핑합니다."""

    status = getattr(response, "status_code", None)
    if status is None or 200 <= int(status) < 400:
        return
    if int(status) >= 500:
        raise MoisServerError(f"{context}: HTTP {status}")
    raise MoisRequestError(f"{context}: HTTP {status}")
