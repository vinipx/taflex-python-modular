from typing import Any, Optional
from taflex.core.drivers.ui_driver import UiDriver
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class AppiumDriver(UiDriver):
    def __init__(self, config: AppConfig):
        self.config = config
        self.driver_type = "Appium Mobile Driver"
        self.driver = None

    def start(self) -> Any:
        logger.info(f"Starting Appium session on {self.config.platform_name}")
        from appium import webdriver
        from appium.options.common.base import AppiumOptions
        
        options = AppiumOptions()
        options.platform_name = self.config.platform_name
        if self.config.device_name:
            options.device_name = self.config.device_name
            
        self.driver = webdriver.Remote(self.config.appium_server_url, options=options)
        return self.driver

    def stop(self) -> None:
        logger.info("Stopping Appium session")
        if self.driver:
            self.driver.quit()

    def navigate(self, url: str) -> None:
        # For mobile, navigate usually means opening a deep link or a URL in a browser
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def click(self, selector: str) -> None:
        logger.info(f"Clicking on: {selector}")
        # In Appium, we usually use find_element first
        # This is a simplified implementation
        from appium.webdriver.common.appiumby import AppiumBy
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=selector).click()

    def type(self, selector: str, text: str) -> None:
        logger.info(f"Typing '{text}' into: {selector}")
        from appium.webdriver.common.appiumby import AppiumBy
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=selector).send_keys(text)

    def get_text(self, selector: str) -> str:
        logger.info(f"Getting text from: {selector}")
        from appium.webdriver.common.appiumby import AppiumBy
        return self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=selector).text

    def is_visible(self, selector: str) -> bool:
        logger.info(f"Checking visibility of: {selector}")
        from appium.webdriver.common.appiumby import AppiumBy
        return self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=selector).is_displayed()

    def wait_for_selector(self, selector: str, timeout_ms: Optional[int] = None) -> Any:
        logger.info(f"Waiting for selector: {selector}")
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from appium.webdriver.common.appiumby import AppiumBy
        
        timeout = (timeout_ms / 1000) if timeout_ms else 30
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, selector))
        )

    def screenshot(self, path: str) -> None:
        logger.info(f"Taking screenshot to: {path}")
        self.driver.save_screenshot(path)
