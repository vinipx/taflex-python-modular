import pytest
from taflex.api.client import HttpxClient
from taflex.core.config.app_config import AppConfig

def test_httpx_client_not_started():
    """Verify that calling methods before start() raises RuntimeError."""
    config = AppConfig(base_url="https://example.com")
    client = HttpxClient(config)
    
    with pytest.raises(RuntimeError, match="Client not started"):
        client.get("/test")
    
    with pytest.raises(RuntimeError, match="Client not started"):
        client.post("/test", json={"key": "value"})

def test_httpx_client_base_url_handling():
    """Verify that base_url is correctly initialized."""
    config = AppConfig(base_url="https://api.example.com")
    client = HttpxClient(config)
    assert client.base_url == "https://api.example.com"
    
    config_no_url = AppConfig(base_url=None)
    client_no_url = HttpxClient(config_no_url)
    assert client_no_url.base_url == ""
