from __future__ import annotations

import pytest

from pymois import (
    get_file_download,
    get_incremental_openapi_endpoint,
    get_openapi_service,
    list_file_downloads,
    list_incremental_openapi_endpoints,
    list_openapi_endpoints,
    list_openapi_services,
    list_response_fields,
)
from pymois.exceptions import MoisCatalogError


def test_openapi_catalog_contains_all_notice_services() -> None:
    services = list_openapi_services()
    assert len(services) == 195
    assert services[0].slug == "hospitals"
    assert services[0].title == "건강_병원"
    assert services[0].application_url == "https://www.data.go.kr/data/15154458/openapi.do"
    assert services[-1].slug == "paid_job_centers"
    assert all(service.application_url.endswith("/openapi.do") for service in services)
    assert len({service.application_url for service in services}) == 195


def test_openapi_endpoint_catalog_has_info_and_history_for_every_service() -> None:
    endpoints = list_openapi_endpoints()
    assert len(endpoints) == 390
    assert len(list_openapi_endpoints(kind="info")) == 195
    assert len(list_openapi_endpoints(kind="history")) == 195
    health = list_openapi_endpoints(category="건강")
    assert {endpoint.service_slug for endpoint in health} >= {"hospitals", "pharmacies"}


def test_incremental_openapi_catalog_matches_all_services() -> None:
    services = {service.slug: service for service in list_openapi_services()}
    endpoints = list_incremental_openapi_endpoints()

    assert len(endpoints) == 195
    assert {endpoint.service_slug for endpoint in endpoints} == set(services)

    first = endpoints[0]
    assert first.service_slug == "hospitals"
    assert first.application_url == services["hospitals"].application_url
    assert first.info_url == services["hospitals"].info_url
    assert first.condition_field == "DAT_UPDT_PNT"
    assert first.source_modified_field == "LAST_MDFCN_PNT"
    assert first.condition_operator == "GTE"
    assert first.get_method == "get_updated_hospitals"
    assert first.iter_method == "iter_updated_hospitals"


def test_incremental_openapi_catalog_filter_and_lookup() -> None:
    health = list_incremental_openapi_endpoints(category="건강")
    assert {endpoint.service_slug for endpoint in health} >= {"hospitals", "pharmacies"}

    hospitals = get_incremental_openapi_endpoint("hospitals")
    assert hospitals.name == "병원"
    assert hospitals.application_url == "https://www.data.go.kr/data/15154458/openapi.do"


def test_file_download_catalog_defaults_to_license_downloads() -> None:
    downloads = list_file_downloads()
    assert len(downloads) == 195
    assert get_file_download("hospitals").download_url.endswith("/file/download/hospitals/info")
    assert len(list_file_downloads(kind=None)) == 208


def test_response_field_catalog_excludes_deleted_by_default() -> None:
    fields = list_response_fields()
    assert all(not field.deleted for field in fields)
    assert any(field.field == "MNG_NO" and field.name == "관리번호" for field in fields)
    with_deleted = list_response_fields(include_deleted=True)
    assert len(with_deleted) == 1011
    assert any(field.local_field == "opnSvcId" and field.deleted for field in with_deleted)


def test_unknown_catalog_entries_raise_clear_error() -> None:
    with pytest.raises(MoisCatalogError):
        get_openapi_service("missing")
    with pytest.raises(MoisCatalogError):
        get_incremental_openapi_endpoint("missing")
    with pytest.raises(MoisCatalogError):
        get_file_download("missing")
