from typing import Any, Optional
from taflex.core.drivers.ui_driver import UiDriver
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class PlaywrightDriver(UiDriver):
    def __init__(self, config: AppConfig):
        self.config = config
        self.driver_type = "Playwright Web Driver"
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self) -> Any:
        logger.info(f"Starting Playwright {self.config.browser} browser (headless={self.config.headless})")
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        
        browser_type = getattr(self.playwright, self.config.browser)
        self.browser = browser_type.launch(headless=self.config.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.timeout_ms)
        return self.page

    def stop(self) -> None:
        logger.info("Stopping Playwright browser")
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def navigate(self, url: str) -> None:
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def click(self, selector: str) -> None:
        logger.info(f"Clicking on: {selector}")
        self.page.click(selector)

    def type(self, selector: str, text: str) -> None:
        logger.info(f"Typing '{text}' into: {selector}")
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        logger.info(f"Getting text from: {selector}")
        return self.page.inner_text(selector)

    def is_visible(self, selector: str) -> bool:
        logger.info(f"Checking visibility of: {selector}")
        return self.page.is_visible(selector)

    def wait_for_selector(self, selector: str, timeout_ms: Optional[int] = None) -> Any:
        logger.info(f"Waiting for selector: {selector}")
        return self.page.wait_for_selector(selector, timeout=timeout_ms)

    def screenshot(self, path: str) -> None:
        logger.info(f"Taking screenshot to: {path}")
        self.page.screenshot(path=path)
