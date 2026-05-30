"""ADR-009 회귀 방지 — `python-kraddr-base`에 의존하지 않는다.

`pyproject.toml`의 dependency, `src/mois/` 소스 임포트, 공개 API 시그니처가
`python-kraddr-base`(`kraddr.base` 패키지)를 끌어들이지 않는지 검증합니다.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

import pytest

import mois
from mois.geocoding import (
    AddressGeocodingProbe,
    _candidate_from_any,
    validate_address_geocoding_probe,
)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "mois"
DEBUG_UI_SRC = ROOT / "packages" / "mois-debug-ui" / "src" / "mois_debug_ui"
FORBIDDEN_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+kraddr\.base[\s.]|import\s+kraddr\.base(?:\s|$))",
    re.MULTILINE,
)


def _iter_source_files() -> list[Path]:
    files: list[Path] = []
    for base in (SRC, DEBUG_UI_SRC):
        if not base.exists():
            continue
        files.extend(path for path in base.rglob("*.py"))
    return files


def test_no_kraddr_base_imports_in_source_tree() -> None:
    """`src/mois/`와 `packages/mois-debug-ui/src/`에 `kraddr.base` 임포트가 없어야 한다."""

    offenders: list[Path] = []
    for path in _iter_source_files():
        if FORBIDDEN_IMPORT_RE.search(path.read_text(encoding="utf-8")):
            offenders.append(path.relative_to(ROOT))
    assert not offenders, (
        f"`kraddr.base` 임포트가 ADR-009를 위반합니다: {offenders}"
    )


def test_pyproject_has_no_kraddr_base_dependency() -> None:
    """`pyproject.toml`의 어떤 dependency 목록에도 `python-kraddr-base`가 없어야 한다."""

    for pyproject_path in (
        ROOT / "pyproject.toml",
        ROOT / "packages" / "mois-debug-ui" / "pyproject.toml",
    ):
        if not pyproject_path.exists():
            continue
        config = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        project = config.get("project", {})
        deps: list[str] = list(project.get("dependencies", []))
        for extras in project.get("optional-dependencies", {}).values():
            deps.extend(extras)
        offenders = [dep for dep in deps if "kraddr-base" in dep or "kraddr_base" in dep]
        assert not offenders, (
            f"{pyproject_path.relative_to(ROOT)}에 python-kraddr-base가 들어 있습니다: {offenders}"
        )


def test_mois_does_not_reexport_kraddr_base_types() -> None:
    """`mois.__all__`에 `PlaceCoordinate`/`Address`/`LatLon`을 노출하지 않는다."""

    forbidden = {"PlaceCoordinate", "Address", "LatLon", "JibunAddress", "RoadNameAddress"}
    leaked = forbidden & set(mois.__all__)
    assert not leaked, f"mois.__all__이 kraddr.base 이름을 재노출합니다: {leaked}"


class _DuckTypedPlaceCoordinate:
    """`kraddr.base.PlaceCoordinate`와 비슷한 속성 구조를 흉내내는 가짜 객체."""

    x = 953243.1
    y = 1954023.1
    road_address = "서울특별시 종로구 자하문로 96"


class _FakeGeocoder:
    def get_coord(self, request: dict[str, Any]) -> list[_DuckTypedPlaceCoordinate]:
        return [_DuckTypedPlaceCoordinate()]

    def nearest_road_address_xy(
        self,
        *,
        x: float,
        y: float,
        max_distance_m: float | None = None,
    ) -> _DuckTypedPlaceCoordinate:
        return _DuckTypedPlaceCoordinate()


def test_candidate_from_any_rejects_arbitrary_objects() -> None:
    """`PlaceCoordinate`/`Address` 모양 객체는 더 이상 자동으로 흡수되지 않는다."""

    with pytest.raises(TypeError, match="GeocodingCandidate"):
        _candidate_from_any(_DuckTypedPlaceCoordinate(), default_crs="EPSG:5179")


def test_validate_helper_rejects_duck_typed_geocoder_results() -> None:
    """검증 helper도 kraddr.base 모양 객체를 받지 않아야 한다."""

    with pytest.raises(TypeError, match="GeocodingCandidate"):
        validate_address_geocoding_probe(
            AddressGeocodingProbe(
                address="서울특별시 종로구 자하문로 96",
                x=953243.1,
                y=1954023.1,
                crs="EPSG:5179",
            ),
            _FakeGeocoder(),
        )
