"""주소 지오코딩 검증용 공개 모델과 helper."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pyproj import Transformer

if TYPE_CHECKING:
    from .db import PlaceRecord

CoordinateCrs = Literal["EPSG:4326", "EPSG:5174", "EPSG:5179"]


class AddressGeocodingProbe(BaseModel):
    """MOIS 주소/좌표 한 행을 외부 지오코더와 비교하기 위한 입력 모델."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    address: str | None = None
    road_address: str | None = None
    lot_address: str | None = None
    x: float | None = None
    y: float | None = None
    lat: float | None = None
    lon: float | None = None
    crs: CoordinateCrs = "EPSG:5174"
    distance_tolerance_m: float = Field(default=100.0, ge=0)
    source_id: str | None = None

    @field_validator("address", "road_address", "lot_address", "source_id", mode="before")
    @classmethod
    def _empty_to_none(cls, value: Any) -> Any:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @classmethod
    def from_place_record(
        cls,
        record: PlaceRecord,
        *,
        distance_tolerance_m: float = 100.0,
    ) -> AddressGeocodingProbe:
        """`PlaceRecord`의 주소와 원본 좌표를 검증 입력으로 변환합니다."""

        return cls(
            source_id=record.mng_no,
            address=record.road_address or record.lot_address,
            road_address=record.road_address,
            lot_address=record.lot_address,
            x=record.source_x,
            y=record.source_y,
            lat=record.lat,
            lon=record.lon,
            crs="EPSG:5174",
            distance_tolerance_m=distance_tolerance_m,
        )

    @property
    def best_address(self) -> str | None:
        """지오코딩 질의에 우선 사용할 주소 문자열."""

        return self.road_address or self.address or self.lot_address


class GeocodingCandidate(BaseModel):
    """검증 대상 지오코더에서 가져온 정규화 후보."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    x: float
    y: float
    crs: CoordinateCrs = "EPSG:5179"
    road_address: str | None = None
    lot_address: str | None = None
    postal_code: str | None = None
    legal_dong_code: str | None = None
    road_name_code: str | None = None
    building_management_number: str | None = None
    building_name: str | None = None
    source: str = ""
    distance_m: float | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class AddressGeocodingValidationResult(BaseModel):
    """MOIS 주소/좌표와 지오코더 결과의 비교 결과."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    source_id: str | None = None
    input_address: str | None = None
    input_x: float | None = None
    input_y: float | None = None
    input_crs: CoordinateCrs
    geocode_candidate: GeocodingCandidate | None = None
    reverse_candidate: GeocodingCandidate | None = None
    geocode_distance_m: float | None = None
    reverse_distance_m: float | None = None
    address_match: bool = False
    within_tolerance: bool = False


class AddressGeocoder(Protocol):
    """주소 검증에 필요한 최소 지오코더 계약."""

    def get_coord(self, request: Mapping[str, Any]) -> Sequence[Any]:
        """주소 문자열을 좌표 후보로 변환합니다."""
        ...

    def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> Any | None:
        """지정 좌표 주변의 가장 가까운 도로명주소 후보를 반환합니다."""
        ...


def validate_address_geocoding_probe(
    probe: AddressGeocodingProbe | Mapping[str, Any],
    geocoder: AddressGeocoder,
    *,
    geocoder_crs: CoordinateCrs = "EPSG:5179",
) -> AddressGeocodingValidationResult:
    """MOIS 주소/좌표 한 행을 지오코더의 정방향/역방향 결과와 비교합니다."""

    dto = (
        probe
        if isinstance(probe, AddressGeocodingProbe)
        else AddressGeocodingProbe.model_validate(probe)
    )
    input_x, input_y = _input_xy(dto, geocoder_crs)

    geocode_candidate = None
    geocode_distance = None
    if dto.best_address:
        matches = geocoder.get_coord(
            {"query": dto.best_address, "limit": 1, "crs": geocoder_crs}
        )
        if matches:
            geocode_candidate = _candidate_from_any(matches[0], default_crs=geocoder_crs)
            if input_x is not None and input_y is not None:
                geocode_distance = _distance(
                    input_x,
                    input_y,
                    geocode_candidate.x,
                    geocode_candidate.y,
                )

    reverse_candidate = None
    reverse_distance = None
    if input_x is not None and input_y is not None:
        result = geocoder.nearest_road_address_xy(
            x=input_x,
            y=input_y,
            max_distance_m=dto.distance_tolerance_m,
        )
        if result is not None:
            reverse_candidate = _candidate_from_any(
                result,
                default_crs=geocoder_crs,
                fallback_x=input_x,
                fallback_y=input_y,
            )
            reverse_distance = reverse_candidate.distance_m

    address_text = dto.best_address or ""
    candidate_address = (
        (geocode_candidate.road_address if geocode_candidate else None)
        or (reverse_candidate.road_address if reverse_candidate else None)
        or ""
    )
    distance_values = [
        value for value in (geocode_distance, reverse_distance) if value is not None
    ]
    return AddressGeocodingValidationResult(
        source_id=dto.source_id,
        input_address=dto.best_address,
        input_x=input_x,
        input_y=input_y,
        input_crs=dto.crs,
        geocode_candidate=geocode_candidate,
        reverse_candidate=reverse_candidate,
        geocode_distance_m=geocode_distance,
        reverse_distance_m=reverse_distance,
        address_match=bool(address_text and address_text in candidate_address),
        within_tolerance=bool(distance_values)
        and min(distance_values) <= dto.distance_tolerance_m,
    )


def _input_xy(
    probe: AddressGeocodingProbe,
    target_crs: CoordinateCrs,
) -> tuple[float | None, float | None]:
    if probe.lat is not None and probe.lon is not None:
        wgs84_y = probe.lat
        wgs84_x = probe.lon
        return _transform_xy(wgs84_x, wgs84_y, "EPSG:4326", target_crs)
    if probe.x is not None and probe.y is not None:
        return _transform_xy(probe.x, probe.y, probe.crs, target_crs)
    return None, None


def _candidate_from_any(
    value: Any,
    *,
    default_crs: CoordinateCrs,
    fallback_x: float | None = None,
    fallback_y: float | None = None,
) -> GeocodingCandidate:
    raw = dict(value) if isinstance(value, Mapping) else _public_attrs(value)
    x = raw.get("x", fallback_x)
    y = raw.get("y", fallback_y)
    if x is None or y is None:
        raise ValueError("지오코딩 후보에는 x/y 좌표가 필요합니다.")
    return GeocodingCandidate(
        x=float(x),
        y=float(y),
        crs=raw.get("crs") or default_crs,
        road_address=raw.get("road_address"),
        lot_address=raw.get("lot_address") or raw.get("parcel_address"),
        postal_code=raw.get("postal_code"),
        legal_dong_code=raw.get("legal_dong_code"),
        road_name_code=raw.get("road_name_code"),
        building_management_number=raw.get("building_management_number"),
        building_name=raw.get("building_name"),
        source=raw.get("source") or "",
        distance_m=raw.get("distance_m"),
        raw=dict(raw.get("raw") or {}),
    )


def _public_attrs(value: Any) -> dict[str, Any]:
    keys = (
        "x",
        "y",
        "crs",
        "road_address",
        "lot_address",
        "parcel_address",
        "postal_code",
        "legal_dong_code",
        "road_name_code",
        "building_management_number",
        "building_name",
        "source",
        "distance_m",
        "raw",
    )
    return {key: getattr(value, key) for key in keys if hasattr(value, key)}


@lru_cache(maxsize=16)
def _transformer(source_crs: str, target_crs: str) -> Transformer:
    return Transformer.from_crs(source_crs, target_crs, always_xy=True)


def _transform_xy(x: float, y: float, source_crs: str, target_crs: str) -> tuple[float, float]:
    if source_crs == target_crs:
        return float(x), float(y)
    transformed_x, transformed_y = _transformer(source_crs, target_crs).transform(
        float(x),
        float(y),
    )
    return float(transformed_x), float(transformed_y)


def _distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
