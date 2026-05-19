from __future__ import annotations

import pytest

from mois import (
    Coordinate,
    CoordinateReferenceSystem,
    KatecPoint,
    StationCoordinates,
    Wgs84Point,
)
from mois.coords import epsg5174_to_wgs84, station_coordinates_from_katec


def test_wgs84_point_uses_lat_lon_order() -> None:
    point = Wgs84Point(lat=37.5665, lon=126.978)

    assert point.as_tuple() == (37.5665, 126.978)
    assert point.to_geojson_position() == (126.978, 37.5665)
    assert point.to_wkt() == "POINT(126.978 37.5665)"
    assert point.crs == CoordinateReferenceSystem.WGS84


def test_wgs84_point_rejects_swapped_or_invalid_order() -> None:
    with pytest.raises(ValueError):
        Wgs84Point(lat=126.978, lon=37.5665)


def test_katec_point_converts_to_wgs84_value_object() -> None:
    katec = KatecPoint(199642.716240024, 452606.614384676)
    lat, lon = epsg5174_to_wgs84(katec.x, katec.y)
    wgs84 = katec.to_wgs84()

    assert katec.as_tuple() == (199642.716240024, 452606.614384676)
    assert wgs84.as_tuple() == (lat, lon)
    assert 126.99 < wgs84.lon < 127.01
    assert 37.57 < wgs84.lat < 37.58


def test_station_coordinates_keep_compatibility_aliases() -> None:
    station = station_coordinates_from_katec(199642.716240024, 452606.614384676)

    assert station.katec_x == station.x
    assert station.katec_y == station.y
    assert station.katec_point.as_tuple() == (station.katec_x, station.katec_y)
    assert station.wgs84_point.as_tuple() == (station.lat, station.lon)
    assert station.to_wkt() == station.wgs84_point.to_wkt()


def test_coordinate_preserves_existing_fields_and_adds_value_objects() -> None:
    coordinate = Coordinate.from_katec(199642.716240024, 452606.614384676)

    assert coordinate.x == coordinate.katec_x
    assert coordinate.y == coordinate.katec_y
    assert coordinate.source_crs == CoordinateReferenceSystem.KATEC
    assert coordinate.target_crs == CoordinateReferenceSystem.WGS84
    assert coordinate.katec_point.as_tuple() == (coordinate.x, coordinate.y)
    assert coordinate.wgs84_point.as_tuple() == (coordinate.lat, coordinate.lon)
    assert isinstance(coordinate.station_coordinates, StationCoordinates)
