"""RustFS 연동 모듈 및 파일 클라이언트의 RustFS 다운로드 기능을 검증하는 단위 테스트."""

from __future__ import annotations

import os
from pathlib import Path
from unittest import mock

import httpx
import pytest
import respx

from mois import (
    AsyncRustfsClient,
    EffectiveRustfsConfig,
    LocalDataFileClient,
    RustfsClient,
)
from mois.rustfs import join_object_key, normalize_object_prefix

CSV_TEXT = (
    "개방자치단체코드,관리번호,인허가일자,영업상태명,사업장명\n"
    "3000000,PHMA1,2025-02-28,영업/정상,포레스트병원\n"
)


def test_effective_rustfs_config_from_env() -> None:
    """환경 변수로부터 설정을 올바르게 로드하는지 테스트합니다."""
    env_mock = {
        "MOIS_RUSTFS_ENABLED": "true",
        "MOIS_RUSTFS_ENDPOINT_URL": "http://rustfs.local:9003",
        "MOIS_RUSTFS_BUCKET": "test-bucket",
        "MOIS_RUSTFS_PREFIX": "test-prefix",
        "MOIS_RUSTFS_REGION": "ap-northeast-2",
        "MOIS_RUSTFS_FORCE_PATH_STYLE": "true",
        "MOIS_RUSTFS_ACCESS_KEY": "test-access-key",
        "MOIS_RUSTFS_SECRET_KEY": "test-secret-key",
    }
    with mock.patch.dict(os.environ, env_mock):
        config = EffectiveRustfsConfig.from_env()
        assert config.enabled is True
        assert config.endpoint_url == "http://rustfs.local:9003"
        assert config.bucket == "test-bucket"
        assert config.prefix == "test-prefix"
        assert config.region == "ap-northeast-2"
        assert config.force_path_style is True
        assert config.access_key == "test-access-key"
        assert config.secret_key == "test-secret-key"
        assert config.credentials_configured is True
        assert config.object_key("slug", "file.zip") == "test-prefix/slug/file.zip"


def test_normalize_object_prefix_and_join_key() -> None:
    """오브젝트 키 정규화 및 조인 헬퍼 함수를 검증합니다."""
    assert normalize_object_prefix("a\\b/c/") == "a/b/c"
    assert normalize_object_prefix("") == "python-mois-api"
    assert join_object_key("prefix", "slug", "file.zip") == "prefix/slug/file.zip"


def test_download_to_rustfs_raises_value_error_if_disabled(tmp_path: Path) -> None:
    """RustFS 연동이 꺼져 있을 때 download_to_rustfs 호출 시 ValueError를 발생하는지 검증합니다."""
    config = EffectiveRustfsConfig(
        enabled=False,
        endpoint_url="http://127.0.0.1:9003",
        bucket="mois",
        prefix="prefix",
        region="us-east-1",
        force_path_style=True,
        access_key="key",
        secret_key="secret",
    )
    
    # download를 mocking하여 로컬 다운로드는 수행되었다고 가정
    class FakeSession:
        def get(self, url: str, **kwargs: object) -> httpx.Response:
            return httpx.Response(200, content=CSV_TEXT.encode("cp949"))

    client = LocalDataFileClient(session=FakeSession())
    
    with pytest.raises(ValueError, match="RustFS가 활성화되어 있지 않습니다"):
        client.download_to_rustfs("hospitals", tmp_path / "test.csv", config=config)


@respx.mock
def test_sync_rustfs_client_put_file_success(tmp_path: Path) -> None:
    """동기식 RustFS 클라이언트가 버킷을 확인하고 파일을 정상적으로 PUT하는지 모킹 테스트합니다."""
    config = EffectiveRustfsConfig(
        enabled=True,
        endpoint_url="http://127.0.0.1:9003",
        bucket="test-bucket",
        prefix="prefix",
        region="us-east-1",
        force_path_style=True,
        access_key="access",
        secret_key="secret",
    )
    
    # HEAD bucket (existence check) -> 200 OK
    respx.head("http://127.0.0.1:9003/test-bucket").mock(return_value=httpx.Response(200))
    # PUT object
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/file.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"etag-value"'})
    )

    test_file = tmp_path / "file.csv"
    test_file.write_text(CSV_TEXT)

    client = RustfsClient(config)
    etag = client.put_file("prefix/hospitals/file.csv", test_file)
    assert etag == "etag-value"


@respx.mock
@pytest.mark.asyncio
async def test_async_rustfs_client_put_file_success(tmp_path: Path) -> None:
    """비동기식 RustFS 클라이언트가 버킷을 확인하고 파일을

    정상적으로 PUT하는지 모킹 테스트합니다.
    """
    config = EffectiveRustfsConfig(
        enabled=True,
        endpoint_url="http://127.0.0.1:9003",
        bucket="test-bucket",
        prefix="prefix",
        region="us-east-1",
        force_path_style=True,
        access_key="access",
        secret_key="secret",
    )
    
    # HEAD bucket (existence check) -> 200 OK
    respx.head("http://127.0.0.1:9003/test-bucket").mock(return_value=httpx.Response(200))
    # PUT object
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/file.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"etag-value"'})
    )

    test_file = tmp_path / "file.csv"
    test_file.write_text(CSV_TEXT)

    client = AsyncRustfsClient(config)
    etag = await client.put_file("prefix/hospitals/file.csv", test_file)
    assert etag == "etag-value"


@respx.mock
def test_local_data_file_client_download_to_rustfs(tmp_path: Path) -> None:
    """LocalDataFileClient를 통해 로컬 다운로드와 RustFS 저장이

    정상적으로 연계 작동하는지 검증합니다.
    """
    config = EffectiveRustfsConfig(
        enabled=True,
        endpoint_url="http://127.0.0.1:9003",
        bucket="test-bucket",
        prefix="prefix",
        region="us-east-1",
        force_path_style=True,
        access_key="access",
        secret_key="secret",
    )
    
    # file.localdata.go.kr 관련 HTTP 모킹 (로컬 다운로드 flow)
    respx.get("https://file.localdata.go.kr/file/hospitals/info").mock(return_value=httpx.Response(200))
    respx.get("https://file.localdata.go.kr/file/validate/download-count").mock(return_value=httpx.Response(200))
    respx.get("https://file.localdata.go.kr/file/download/hospitals/info").mock(
        return_value=httpx.Response(200, content=CSV_TEXT.encode("cp949"))
    )

    # RustFS 관련 HTTP 모킹 (HEAD, PUT)
    respx.head("http://127.0.0.1:9003/test-bucket").mock(return_value=httpx.Response(200))
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/hospitals.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"mock-etag"'})
    )
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/hospitals_dyn.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"mock-etag"'})
    )

    client = LocalDataFileClient()
    local_path = tmp_path / "hospitals.csv"
    
    # download_to_rustfs 명시적 호출
    uri = client.download_to_rustfs("hospitals", local_path, config=config)
    assert uri == "rustfs://test-bucket/prefix/hospitals/hospitals.csv"
    assert local_path.exists()
    assert local_path.read_text(encoding="cp949") == CSV_TEXT

    # 동적 편의 메서드 호출 (__getattr__ 검증)
    local_path_dynamic = tmp_path / "hospitals_dyn.csv"
    uri_dyn = client.download_hospitals_to_rustfs(local_path_dynamic, config=config)
    assert uri_dyn == "rustfs://test-bucket/prefix/hospitals/hospitals_dyn.csv"
    assert local_path_dynamic.exists()


@respx.mock
@pytest.mark.asyncio
async def test_async_local_data_file_client_download_to_rustfs(tmp_path: Path) -> None:
    """AsyncLocalDataFileClient를 통해 로컬 다운로드와 RustFS 저장이

    정상적으로 연계 작동하는지 검증합니다.
    """
    config = EffectiveRustfsConfig(
        enabled=True,
        endpoint_url="http://127.0.0.1:9003",
        bucket="test-bucket",
        prefix="prefix",
        region="us-east-1",
        force_path_style=True,
        access_key="access",
        secret_key="secret",
    )
    
    # file.localdata.go.kr 관련 HTTP 모킹 (로컬 다운로드 flow)
    respx.get("https://file.localdata.go.kr/file/hospitals/info").mock(return_value=httpx.Response(200))
    respx.get("https://file.localdata.go.kr/file/validate/download-count").mock(return_value=httpx.Response(200))
    respx.get("https://file.localdata.go.kr/file/download/hospitals/info").mock(
        return_value=httpx.Response(200, content=CSV_TEXT.encode("cp949"))
    )

    # RustFS 관련 HTTP 모킹 (HEAD, PUT)
    respx.head("http://127.0.0.1:9003/test-bucket").mock(return_value=httpx.Response(200))
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/hospitals.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"mock-etag"'})
    )
    respx.put("http://127.0.0.1:9003/test-bucket/prefix/hospitals/hospitals_dyn.csv").mock(
        return_value=httpx.Response(200, headers={"etag": '"mock-etag"'})
    )

    async with LocalDataFileClient.aio() as client:
        local_path = tmp_path / "hospitals.csv"
        
        # download_to_rustfs 명시적 호출
        uri = await client.download_to_rustfs("hospitals", local_path, config=config)
        assert uri == "rustfs://test-bucket/prefix/hospitals/hospitals.csv"
        assert local_path.exists()
        assert local_path.read_text(encoding="cp949") == CSV_TEXT

        # 동적 편의 메서드 호출 (__getattr__ 검증)
        local_path_dynamic = tmp_path / "hospitals_dyn.csv"
        uri_dyn = await client.download_hospitals_to_rustfs(local_path_dynamic, config=config)
        assert uri_dyn == "rustfs://test-bucket/prefix/hospitals/hospitals_dyn.csv"
        assert local_path_dynamic.exists()
