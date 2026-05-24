"""좌표계 변환."""

from __future__ import annotations

from functools import lru_cache

from pyproj import Transformer

from .models import KatecPoint, StationCoordinates, Wgs84Point


@lru_cache(maxsize=1)
def _epsg5174_to_wgs84_transformer() -> Transformer:
    return Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)


def epsg5174_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Bessel 중부원점TM(EPSG:5174) `(x, y)`를 WGS84 `(lat, lon)`로 변환합니다."""

    transformed_lon, transformed_lat = _epsg5174_to_wgs84_transformer().transform(
        float(x),
        float(y),
    )
    return float(transformed_lat), float(transformed_lon)


def katec_to_wgs84_point(point: KatecPoint) -> Wgs84Point:
    """KATEC `KatecPoint(x, y)`를 WGS84 `Wgs84Point(lat, lon)`로 변환합니다."""

    lat, lon = epsg5174_to_wgs84(point.x, point.y)
    return Wgs84Point(lat=lat, lon=lon)


def epsg5174_to_wgs84_point(x: float, y: float) -> Wgs84Point:
    """EPSG:5174 `(x, y)`를 WGS84 값 객체로 변환합니다."""

    return katec_to_wgs84_point(KatecPoint(x, y))


def station_coordinates_from_katec(x: float, y: float) -> StationCoordinates:
    """EPSG:5174 `(x, y)`에서 KATEC/WGS84 복합 좌표 객체를 생성합니다."""

    return StationCoordinates.from_katec(x, y)
