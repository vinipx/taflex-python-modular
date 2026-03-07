import pytest
from unittest.mock import MagicMock
from taflex.core.drivers.base_page import BasePage

def test_base_page_initialization():
    """Verify BasePage initializes with a driver."""
    mock_driver = MagicMock()
    page = BasePage(mock_driver)
    assert page.driver == mock_driver

def test_base_page_navigate_to():
    """Verify navigate_to calls the driver's navigate method."""
    mock_driver = MagicMock()
    page = BasePage(mock_driver)
    page.navigate_to("https://example.com")
    mock_driver.navigate.assert_called_once_with("https://example.com")

def test_base_page_is_at():
    """Verify is_at calls the driver's is_visible method."""
    mock_driver = MagicMock()
    mock_driver.is_visible.return_value = True
    page = BasePage(mock_driver)
    
    result = page.is_at(".unique-element")
    assert result is True
    mock_driver.is_visible.assert_called_once_with(".unique-element")
