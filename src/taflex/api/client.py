from typing import Any, Optional
import httpx
from taflex.core.drivers.api_client import ApiClient
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class HttpxClient(ApiClient):
    def __init__(self, config: AppConfig):
        self.config = config
        self.driver_type = "HTTPX API Client"
        self.base_url = config.base_url or ""
        self.client: Optional[httpx.Client] = None

    def start(self) -> "HttpxClient":
        logger.info(f"Starting HTTPX client with base_url={self.base_url}")
        self.client = httpx.Client(base_url=self.base_url)
        return self

    def stop(self) -> None:
        logger.info("Closing HTTPX client")
        if self.client:
            self.client.close()

    def get(self, url: str, **kwargs) -> httpx.Response:
        logger.info(f"GET request to: {url}")
        if not self.client:
            raise RuntimeError("Client not started. Call .start() first.")
        return self.client.get(url, **kwargs)

    def post(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> httpx.Response:
        logger.info(f"POST request to: {url}")
        if not self.client:
            raise RuntimeError("Client not started. Call .start() first.")
        return self.client.post(url, data=data, json=json, **kwargs)

    def put(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> httpx.Response:
        logger.info(f"PUT request to: {url}")
        if not self.client:
            raise RuntimeError("Client not started. Call .start() first.")
        return self.client.put(url, data=data, json=json, **kwargs)

    def patch(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> httpx.Response:
        logger.info(f"PATCH request to: {url}")
        if not self.client:
            raise RuntimeError("Client not started. Call .start() first.")
        return self.client.patch(url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        logger.info(f"DELETE request to: {url}")
        if not self.client:
            raise RuntimeError("Client not started. Call .start() first.")
        return self.client.delete(url, **kwargs)
