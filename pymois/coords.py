"""좌표계 변환."""

from __future__ import annotations

from functools import lru_cache

from pyproj import Transformer


@lru_cache(maxsize=1)
def _epsg5174_to_wgs84_transformer() -> Transformer:
    return Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)


def epsg5174_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Bessel 중부원점TM(EPSG:5174) 좌표를 WGS84 경도/위도로 변환합니다."""

    lon, lat = _epsg5174_to_wgs84_transformer().transform(float(x), float(y))
    return float(lon), float(lat)
