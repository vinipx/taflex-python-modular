import pytest
from unittest.mock import patch
from taflex.contract.pact_manager import PactManager
from taflex.core.config.app_config import AppConfig

@pytest.fixture
def mock_config():
    return AppConfig(
        pact_consumer="test-consumer",
        pact_provider="test-provider",
        pact_dir="test-pacts"
    )

@patch("taflex.contract.pact_manager.Pact")
def test_pact_manager_initialization(mock_pact_class, mock_config):
    """Verify PactManager initializes Pact correctly."""
    manager = PactManager(mock_config)
    
    mock_pact_class.assert_called_once_with(
        consumer="test-consumer",
        provider="test-provider",
        pact_dir="test-pacts"
    )
    assert manager.pact == mock_pact_class.return_value

@patch("taflex.contract.pact_manager.Pact")
def test_pact_manager_methods(mock_pact_class, mock_config):
    """Verify PactManager methods delegate to the underlying Pact object."""
    manager = PactManager(mock_config)
    mock_pact = manager.pact
    
    # Test start/stop
    manager.start_service()
    mock_pact.start_service.assert_called_once()
    
    manager.stop_service()
    mock_pact.stop_service.assert_called_once()
    
    # Test DSL methods (fluid interface)
    result = (manager
              .given("state")
              .upon_receiving("scenario")
              .with_request("GET", "/path")
              .will_respond_with(200))
    
    assert result == manager
    mock_pact.given.assert_called_once_with("state")
    mock_pact.upon_receiving.assert_called_once_with("scenario")
    mock_pact.with_request.assert_called_once_with("GET", "/path", None, None, None)
    mock_pact.will_respond_with.assert_called_once_with(200, None, None)
    
    # Test verify
    manager.verify()
    mock_pact.verify.assert_called_once()

@patch("taflex.contract.pact_manager.Pact")
def test_pact_manager_uri(mock_pact_class, mock_config):
    """Verify PactManager exposed the mock service URI."""
    manager = PactManager(mock_config)
    manager.pact.uri = "http://localhost:1234"
    assert manager.uri == "http://localhost:1234"
