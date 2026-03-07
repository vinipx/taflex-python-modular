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

    def start(self):
        logger.info(f"Starting Playwright {self.config.browser} browser (headless={self.config.headless})")
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright().start()
        
        browser_type = getattr(self.playwright, self.config.browser)
        self.browser = browser_type.launch(headless=self.config.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.timeout_ms)
        return self.page

    def stop(self):
        logger.info("Stopping Playwright browser")
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
