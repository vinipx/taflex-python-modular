import pytest
from unittest.mock import patch
from taflex.core.drivers.driver_factory import DriverFactory
from taflex.core.config.app_config import AppConfig

def test_driver_factory_creates_web_driver():
    """Verify DriverFactory creates PlaywrightDriver for 'web' mode."""
    config = AppConfig(execution_mode="web")
    
    with patch("taflex.web.driver.PlaywrightDriver") as mock_driver:
        DriverFactory.create(config)
        mock_driver.assert_called_once_with(config)

def test_driver_factory_creates_api_driver():
    """Verify DriverFactory creates HttpxClient for 'api' mode."""
    config = AppConfig(execution_mode="api")
    
    with patch("taflex.api.client.HttpxClient") as mock_client:
        DriverFactory.create(config)
        mock_client.assert_called_once_with(config)

def test_driver_factory_creates_mobile_driver():
    """Verify DriverFactory creates AppiumDriver for 'mobile' mode."""
    config = AppConfig(execution_mode="mobile")
    
    with patch("taflex.mobile.driver.AppiumDriver") as mock_driver:
        DriverFactory.create(config)
        mock_driver.assert_called_once_with(config)

def test_driver_factory_unsupported_mode():
    """Verify DriverFactory raises ValueError for unsupported modes."""
    config = AppConfig(execution_mode="invalid_mode")
    
    with pytest.raises(ValueError, match="Unsupported execution mode: invalid_mode"):
        DriverFactory.create(config)

def test_driver_factory_missing_module():
    """Verify DriverFactory raises ImportError if the module cannot be loaded (simulated)."""
    config = AppConfig(execution_mode="web")
    
    # Simulate an error during import
    with patch("taflex.web.driver.PlaywrightDriver", side_effect=ImportError("Mocked import error")):
        with pytest.raises(ImportError, match="Mocked import error"):
            DriverFactory.create(config)
