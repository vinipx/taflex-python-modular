import pytest
from unittest.mock import MagicMock, patch

# Load the fixtures from the core conftest
pytest_plugins = ["taflex.core.conftest"]

# Create a global mock for the factory to verify how it's called
mock_factory_create = MagicMock()
mock_driver_instance = MagicMock()

@pytest.fixture
def patch_driver_factory(monkeypatch):
    """
    Patch the DriverFactory inside the conftest module before any test runs.
    This ensures the `driver` fixture will call our mock instead of trying
    to launch real browsers or API clients.
    """
    mock_factory_create.reset_mock()
    mock_driver_instance.reset_mock()
    
    mock_factory_create.return_value = mock_driver_instance
    monkeypatch.setattr('taflex.core.drivers.driver_factory.DriverFactory.create', mock_factory_create)


@pytest.mark.api
def test_driver_fixture_api_marker(patch_driver_factory, driver):
    """Test that @pytest.mark.api overrides the execution_mode to 'api'."""
    mock_factory_create.assert_called_once()
    config = mock_factory_create.call_args[0][0]
    assert config.execution_mode == "api"
    mock_driver_instance.start.assert_called_once()


@pytest.mark.web
def test_driver_fixture_web_marker(patch_driver_factory, driver):
    """Test that @pytest.mark.web overrides the execution_mode to 'web'."""
    mock_factory_create.assert_called_once()
    config = mock_factory_create.call_args[0][0]
    assert config.execution_mode == "web"


@pytest.mark.mobile
def test_driver_fixture_mobile_marker(patch_driver_factory, driver):
    """Test that @pytest.mark.mobile overrides the execution_mode to 'mobile'."""
    mock_factory_create.assert_called_once()
    config = mock_factory_create.call_args[0][0]
    assert config.execution_mode == "mobile"


@pytest.mark.api
@pytest.mark.web
def test_driver_fixture_multiple_markers_precedence(patch_driver_factory, driver):
    """
    Edge case: multiple markers applied to a test.
    The fixture logic checks 'api' > 'web' > 'mobile'.
    So 'api' should take precedence.
    """
    mock_factory_create.assert_called_once()
    config = mock_factory_create.call_args[0][0]
    assert config.execution_mode == "api"


def test_driver_fixture_no_marker_uses_env(patch_driver_factory, monkeypatch):
    """
    Test that without markers, the fixture uses the environment config.
    To test this cleanly, we invoke the fixture's logic directly.
    """
    from taflex.core.conftest import driver as driver_fixture
    from taflex.core.config.app_config import AppConfig

    request_mock = MagicMock()
    request_mock.node.get_closest_marker.return_value = None

    # Patch AppConfig to return a specific mode
    mock_config = AppConfig(execution_mode="mobile")
    
    with patch('taflex.core.config.app_config.AppConfig', return_value=mock_config):
        # Unwrap fixture
        original_fixture_func = getattr(driver_fixture, "__wrapped__", driver_fixture)
        
        gen = original_fixture_func(request_mock)
        next(gen)
        
        mock_factory_create.assert_called_once()
        config = mock_factory_create.call_args[0][0]
        assert config.execution_mode == "mobile"


def test_driver_fixture_negative_invalid_mode():
    """Negative case: No marker provided and an invalid execution mode in the environment."""
    from taflex.core.conftest import driver as driver_fixture
    from taflex.core.config.app_config import AppConfig
    from taflex.core.drivers.driver_factory import DriverFactory

    request_mock = MagicMock()
    request_mock.node.get_closest_marker.return_value = None

    # Patch AppConfig to simulate invalid configuration
    mock_config = AppConfig(execution_mode="invalid_mode")
    
    with patch('taflex.core.config.app_config.AppConfig', return_value=mock_config):
        with patch('taflex.core.drivers.driver_factory.DriverFactory.create', side_effect=DriverFactory.create):
            original_fixture_func = getattr(driver_fixture, "__wrapped__", driver_fixture)
            
            with pytest.raises(ValueError, match="Unsupported execution mode: invalid_mode"):
                gen = original_fixture_func(request_mock)
                next(gen)
