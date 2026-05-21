from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mois import (
    AddressGeocodingProbe,
    GeocodingCandidate,
    validate_address_geocoding_probe,
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
