"""주소 지오코딩 검증용 공개 모델과 helper.

`python-mois-api`는 주소 정규화·정/역 지오코딩을 자체 구현하지 않습니다(ADR-002).
외부 라이브러리 [`python-kraddr-geo`](https://github.com/digitie/python-kraddr-geo)의
`AsyncAddressClient` 같은 클라이언트로 후보를 받아온 뒤, 여기에 정의된
`validate_address_geocoding_probe[_async]`로 MOIS 인허가 원본 좌표·주소와 비교만 합니다.
신규 보강 필드는 `kraddr-geo`의 `x_extension`을 통해 받습니다.

자세한 통합 방법은 `docs/integration-with-kraddr-geo.md`와
`docs/decisions.md` ADR-002/003/004를 참조하세요.
"""

from __future__ import annotations

import math
import re
from collections.abc import Awaitable, Mapping, Sequence
from functools import lru_cache
from inspect import isawaitable
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
    """주소 검증에 필요한 최소 지오코더 계약.

    동기/비동기 구현을 모두 허용하기 위해 반환 타입을 동기 값 또는 awaitable로 둡니다.
    `python-kraddr-geo`처럼 async-only 구현은 코루틴을 반환하면 됩니다(ADR-004 참조).
    """

    def get_coord(
        self,
        request: Mapping[str, Any],
    ) -> Sequence[Any] | Awaitable[Sequence[Any]]:
        """주소 문자열을 좌표 후보로 변환합니다."""
        ...

    def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> Any | None | Awaitable[Any | None]:
        """지정 좌표 주변의 가장 가까운 도로명주소 후보를 반환합니다."""
        ...


def validate_address_geocoding_probe(
    probe: AddressGeocodingProbe | Mapping[str, Any],
    geocoder: AddressGeocoder,
    *,
    geocoder_crs: CoordinateCrs = "EPSG:5179",
) -> AddressGeocodingValidationResult:
    """MOIS 주소/좌표 한 행을 지오코더의 정방향/역방향 결과와 비교합니다.

    지오코더 메서드가 코루틴을 반환하면 `TypeError`로 거부합니다. async 구현
    (`python-kraddr-geo`의 `AsyncAddressClient` 등)을 검증할 때는
    `validate_address_geocoding_probe_async`를 사용합니다.
    """

    dto = _coerce_probe(probe)
    input_x, input_y = _input_xy(dto, geocoder_crs)

    geocode_candidate = None
    geocode_distance = None
    if dto.best_address:
        matches = geocoder.get_coord(
            {"query": dto.best_address, "limit": 1, "crs": geocoder_crs}
        )
        if isawaitable(matches):
            raise TypeError(
                "비동기 지오코더는 validate_address_geocoding_probe_async를 사용해야 합니다"
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
        if isawaitable(result):
            raise TypeError(
                "비동기 지오코더는 validate_address_geocoding_probe_async를 사용해야 합니다"
            )
        if result is not None:
            reverse_candidate = _candidate_from_any(
                result,
                default_crs=geocoder_crs,
                fallback_x=input_x,
                fallback_y=input_y,
            )
            reverse_distance = reverse_candidate.distance_m

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
        address_match=_addresses_match(dto.best_address, geocode_candidate, reverse_candidate),
        within_tolerance=bool(distance_values)
        and min(distance_values) <= dto.distance_tolerance_m,
    )


async def validate_address_geocoding_probe_async(
    probe: AddressGeocodingProbe | Mapping[str, Any],
    geocoder: AddressGeocoder,
    *,
    geocoder_crs: CoordinateCrs = "EPSG:5179",
) -> AddressGeocodingValidationResult:
    """`validate_address_geocoding_probe`의 비동기 버전.

    `python-kraddr-geo`의 `AsyncAddressClient` 같은 async-only 클라이언트(ADR-004)를
    그대로 사용할 수 있도록 코루틴 결과를 `await`합니다.
    """

    dto = _coerce_probe(probe)
    input_x, input_y = _input_xy(dto, geocoder_crs)

    geocode_candidate = None
    geocode_distance = None
    if dto.best_address:
        matches = await _maybe_await(
            geocoder.get_coord(
                {"query": dto.best_address, "limit": 1, "crs": geocoder_crs}
            )
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
        result = await _maybe_await(
            geocoder.nearest_road_address_xy(
                x=input_x,
                y=input_y,
                max_distance_m=dto.distance_tolerance_m,
            )
        )
        if result is not None:
            reverse_candidate = _candidate_from_any(
                result,
                default_crs=geocoder_crs,
                fallback_x=input_x,
                fallback_y=input_y,
            )
            reverse_distance = reverse_candidate.distance_m

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
        address_match=_addresses_match(dto.best_address, geocode_candidate, reverse_candidate),
        within_tolerance=bool(distance_values)
        and min(distance_values) <= dto.distance_tolerance_m,
    )


async def _maybe_await(value: Any) -> Any:
    if isawaitable(value):
        return await value
    return value


def _coerce_probe(
    probe: AddressGeocodingProbe | Mapping[str, Any],
) -> AddressGeocodingProbe:
    if isinstance(probe, AddressGeocodingProbe):
        return probe
    return AddressGeocodingProbe.model_validate(probe)


def _addresses_match(
    input_address: str | None,
    geocode_candidate: GeocodingCandidate | None,
    reverse_candidate: GeocodingCandidate | None,
) -> bool:
    """입력 주소와 후보 주소를 공백/구두점 무시 양방향 substring 매칭으로 비교합니다."""

    if not input_address:
        return False
    needle = _normalize_address(input_address)
    if not needle:
        return False
    for candidate in (geocode_candidate, reverse_candidate):
        if candidate is None:
            continue
        for text_value in (candidate.road_address, candidate.lot_address):
            haystack = _normalize_address(text_value)
            if not haystack:
                continue
            if needle in haystack or haystack in needle:
                return True
    return False


_ADDRESS_NOISE_RE = re.compile(r"[\s,.\-()\[\]/]+")


def _normalize_address(value: str | None) -> str:
    if not value:
        return ""
    return _ADDRESS_NOISE_RE.sub("", value).casefold()


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
