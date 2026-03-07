from taflex.core.drivers.ui_driver import UiDriver

class BasePage:
    """
    Base class for all Page Objects in the framework.
    This class provides a common interface and shared logic for both Web and Mobile pages.
    """
    def __init__(self, driver: UiDriver):
        self.driver = driver

    def navigate_to(self, url: str):
        """Navigate to a specific URL."""
        self.driver.navigate(url)

    def is_at(self, selector: str) -> bool:
        """Check if a specific element (identifying the page) is visible."""
        return self.driver.is_visible(selector)
