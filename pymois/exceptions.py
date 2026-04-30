"""pymois 예외 계층."""

from __future__ import annotations


class MoisError(Exception):
    """pymois 공통 예외."""


class MoisAuthError(MoisError):
    """인증키가 없거나 거부된 경우."""


class MoisRequestError(MoisError):
    """요청 파라미터, HTTP 4xx, 제한 초과 등 클라이언트 계열 오류."""


class MoisServerError(MoisError):
    """MOIS/data.go.kr/localdata 서버 오류 또는 일시 장애."""


class MoisParseError(MoisError):
    """응답 또는 파일을 예상한 구조로 해석할 수 없는 경우."""


class MoisCatalogError(MoisError):
    """알 수 없는 API/파일 카탈로그 항목을 요청한 경우."""
