from taflex.core.drivers.ui_driver import UiDriver
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class AppiumDriver(UiDriver):
    def __init__(self, config: AppConfig):
        self.config = config
        self.driver_type = "Appium Mobile Driver"
        self.driver = None

    def start(self):
        logger.info(f"Starting Appium session on {self.config.platform_name}")
        from appium import webdriver
        from appium.options.common.base import AppiumOptions
        
        options = AppiumOptions()
        options.platform_name = self.config.platform_name
        if self.config.device_name:
            options.device_name = self.config.device_name
            
        self.driver = webdriver.Remote(self.config.appium_server_url, options=options)
        return self.driver

    def stop(self):
        logger.info("Stopping Appium session")
        if self.driver:
            self.driver.quit()
