import pytest
pytest.importorskip("playwright", reason="playwright module not found. Skipping web driver tests as it was likely not included in scaffolding.")

from unittest.mock import MagicMock, patch
from taflex.web.driver import PlaywrightDriver
from taflex.core.config.app_config import AppConfig

def test_playwright_driver_uninitialized_methods():
    """Verify behavior when interaction methods are called before start() (will raise AttributeError on self.page)."""
    config = AppConfig()
    driver = PlaywrightDriver(config)
    
    # self.page is None initially
    with pytest.raises(AttributeError):
        driver.navigate("https://example.com")

@patch("playwright.sync_api.sync_playwright")
def test_playwright_driver_start_stop(mock_sync):
    """Verify the start/stop sequence and resource management."""
    mock_playwright = MagicMock()
    mock_sync.return_value.start.return_value = mock_playwright
    
    config = AppConfig(browser="chromium", headless=True)
    driver = PlaywrightDriver(config)
    
    # Mocking browser launch
    mock_browser = MagicMock()
    getattr(mock_playwright, "chromium").launch.return_value = mock_browser
    
    driver.start()
    
    assert driver.playwright is not None
    assert driver.browser is not None
    
    driver.stop()
    
    mock_browser.close.assert_called_once()
    mock_playwright.stop.assert_called_once()
