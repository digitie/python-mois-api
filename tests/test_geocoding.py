from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

import pytest

from mois import (
    AddressGeocodingProbe,
    GeocodingCandidate,
    validate_address_geocoding_probe,
    validate_address_geocoding_probe_async,
)


@dataclass(frozen=True)
class ReverseCandidate:
    x: float
    y: float
    road_address: str
    source: str
    distance_m: float
    raw: dict[str, Any]


class FakeGeocoder:
    def get_coord(self, request: dict[str, Any]) -> list[GeocodingCandidate]:
        assert request["crs"] == "EPSG:5179"
        return [
            GeocodingCandidate(
                x=953243.1,
                y=1954023.1,
                road_address="Seoul Jongno-gu Jahamun-ro 96 (Pyeongan)",
                source="fixture",
            )
        ]

    def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> ReverseCandidate:
        assert max_distance_m == 2
        return ReverseCandidate(
            x=x,
            y=y,
            road_address="Seoul Jongno-gu Jahamun-ro 96 (Pyeongan)",
            source="fixture",
            distance_m=0.0,
            raw={"source_id": "nearest-1"},
        )


def test_validate_address_geocoding_probe_compares_address_and_distance() -> None:
    result = validate_address_geocoding_probe(
        AddressGeocodingProbe(
            source_id="mois-1",
            address="Seoul Jongno-gu Jahamun-ro 96 (Pyeongan)",
            x=953243.1,
            y=1954023.1,
            crs="EPSG:5179",
            distance_tolerance_m=2,
        ),
        FakeGeocoder(),
    )

    assert result.source_id == "mois-1"
    assert result.address_match is True
    assert result.within_tolerance is True
    assert result.geocode_distance_m == 0
    assert result.reverse_distance_m == 0


def test_address_geocoding_probe_prefers_road_address() -> None:
    probe = AddressGeocodingProbe(
        address="지번 주소",
        road_address="도로명 주소",
        lot_address="소재지 주소",
    )

    assert probe.best_address == "도로명 주소"


def test_address_geocoding_probe_exposes_lat_before_lon() -> None:
    fields = list(AddressGeocodingProbe.model_fields)

    assert fields.index("lat") < fields.index("lon")


class AsyncFakeGeocoder:
    async def get_coord(self, request: dict[str, Any]) -> list[GeocodingCandidate]:
        assert request["crs"] == "EPSG:5179"
        return [
            GeocodingCandidate(
                x=953243.1,
                y=1954023.1,
                road_address="서울특별시 종로구 자하문로 96",
                source="kraddr-geo",
            )
        ]

    async def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> ReverseCandidate:
        return ReverseCandidate(
            x=x,
            y=y,
            road_address="서울특별시 종로구 자하문로 96",
            source="kraddr-geo",
            distance_m=0.0,
            raw={},
        )


def test_validate_async_supports_kraddr_geo_style_client() -> None:
    async def run() -> None:
        result = await validate_address_geocoding_probe_async(
            AddressGeocodingProbe(
                source_id="mois-2",
                address="서울특별시 종로구 자하문로 96 (평안)",
                x=953243.1,
                y=1954023.1,
                crs="EPSG:5179",
                distance_tolerance_m=5,
            ),
            AsyncFakeGeocoder(),
        )
        assert result.within_tolerance is True
        assert result.address_match is True

    asyncio.run(run())


def test_validate_sync_rejects_async_geocoder() -> None:
    geocoder = AsyncFakeGeocoder()
    with (
        pytest.warns(RuntimeWarning, match="coroutine"),
        pytest.raises(TypeError, match="validate_address_geocoding_probe_async"),
    ):
        validate_address_geocoding_probe(
            AddressGeocodingProbe(address="서울특별시 종로구 자하문로 96"),
            geocoder,
        )


class KoreanGeocoder:
    def get_coord(self, request: dict[str, Any]) -> list[GeocodingCandidate]:
        return [
            GeocodingCandidate(
                x=953243.1,
                y=1954023.1,
                road_address="서울특별시 종로구 자하문로 96",
                source="fixture",
            )
        ]

    def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> ReverseCandidate:
        return ReverseCandidate(
            x=x,
            y=y,
            road_address="서울특별시 종로구 자하문로 96",
            source="fixture",
            distance_m=0.0,
            raw={},
        )


def test_address_match_ignores_whitespace_and_punctuation() -> None:
    result = validate_address_geocoding_probe(
        AddressGeocodingProbe(
            address="서울특별시 종로구 자하문로 96 (평안)",
            x=953243.1,
            y=1954023.1,
            crs="EPSG:5179",
            distance_tolerance_m=2,
        ),
        KoreanGeocoder(),
    )

    assert result.address_match is True
