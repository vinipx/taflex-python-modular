from taflex.core.drivers.api_client import ApiClient
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class HttpxClient(ApiClient):
    def __init__(self, config: AppConfig):
        self.config = config
        self.driver_type = "HTTPX API Client"
        self.base_url = config.base_url or ""
        self.client = None

    def start(self):
        import httpx
        logger.info(f"Starting HTTPX client with base_url={self.base_url}")
        self.client = httpx.Client(base_url=self.base_url)
        return self

    def stop(self):
        logger.info("Closing HTTPX client")
        if self.client:
            self.client.close()

    def get(self, url, **kwargs):
        logger.info(f"GET request to: {url}")
        return self.client.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        logger.info(f"POST request to: {url}")
        return self.client.post(url, data=data, json=json, **kwargs)
