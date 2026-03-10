import os
import pytest
from typing import Generator
from dotenv import load_dotenv

# Ensure .env is loaded into os.environ for external plugins (like pytest-jira-xray)
load_dotenv()

from taflex.core.config.app_config import AppConfig  # noqa: E402

@pytest.fixture(scope="session")
def base_config() -> AppConfig:
    """Session-scoped fixture to provide the base application configuration."""
    return AppConfig()

def pytest_configure(config):
    """Register markers and configure reporting integrations."""
    config.addinivalue_line("markers", "api: mark test as api test")
    config.addinivalue_line("markers", "web: mark test as web test")
    config.addinivalue_line("markers", "mobile: mark test as mobile test")
    config.addinivalue_line("markers", "bdd: mark test as bdd test")

    # Load configuration once for reporting setup
    app_config = AppConfig()
    
    if "reportportal" in app_config.reporters:
        if app_config.rp_api_key == "your_secret_api_key" or not app_config.rp_api_key:
            import logging
            logging.warning("ReportPortal reporting is enabled in .env, but using dummy or empty credentials. Disabling ReportPortal for this run.")
        else:
            config.option.rp_enabled = True
            config.option.rp_endpoint = app_config.rp_endpoint
            config.option.rp_api_key = app_config.rp_api_key or app_config.rp_uuid
            config.option.rp_project = app_config.rp_project
            config.option.rp_launch = app_config.rp_launch

    if "xray" in app_config.reporters:
        # Prevent crash if user hasn't configured real credentials yet
        if app_config.xray_client_id == "your_xray_client_id" or not app_config.xray_client_id:
            import logging
            logging.warning("Xray reporting is enabled in .env, but using dummy or empty credentials. Disabling Xray for this run.")
        else:
            config.option.jira_xray = True
            config.option.client_secret_auth = True
            if "cloud" in os.environ.get("XRAY_API_BASE_URL", "cloud"):
                config.option.cloud = True

def _manage_driver_lifecycle(config_instance: AppConfig) -> Generator:
    """Helper to manage the full lifecycle of a driver instance."""
    from taflex.core.drivers.driver_factory import DriverFactory
    
    driver_instance = DriverFactory.create(config_instance)
    driver_instance.start()
    
    yield driver_instance
    
    driver_instance.stop()

@pytest.fixture
def web_driver(base_config: AppConfig):
    """Fixture for explicit Web UI testing."""
    config = base_config.model_copy(update={'execution_mode': 'web'})
    yield from _manage_driver_lifecycle(config)

@pytest.fixture
def api_driver(base_config: AppConfig):
    """Fixture for explicit API testing."""
    config = base_config.model_copy(update={'execution_mode': 'api'})
    yield from _manage_driver_lifecycle(config)

@pytest.fixture
def mobile_driver(base_config: AppConfig):
    """Fixture for explicit Mobile testing."""
    config = base_config.model_copy(update={'execution_mode': 'mobile'})
    yield from _manage_driver_lifecycle(config)

@pytest.fixture
def driver(request, base_config: AppConfig):
    """Generic driver fixture that resolves strategy via markers or config."""
    config = base_config.model_copy()

    # Override execution_mode if marker is present
    if request.node.get_closest_marker("api"):
        config.execution_mode = "api"
    elif request.node.get_closest_marker("web"):
        config.execution_mode = "web"
    elif request.node.get_closest_marker("mobile"):
        config.execution_mode = "mobile"

    yield from _manage_driver_lifecycle(config)

@pytest.fixture
def pact(base_config: AppConfig):
    """Fixture for Pact contract testing."""
    from taflex.contract.pact_manager import PactManager
    
    pact_manager = PactManager(base_config)
    pact_manager.start_service()
    
    yield pact_manager
    
    pact_manager.stop_service()

@pytest.fixture(scope="session")
def mq_client(base_config: AppConfig):
    if base_config.mq_protocol == "rabbitmq":
        from taflex.mq.rabbitmq_client import RabbitMQClient
        client = RabbitMQClient(base_config)
    elif base_config.mq_protocol == "kafka":
        from taflex.mq.kafka_client import KafkaClient
        client = KafkaClient(base_config)
    else:
        raise ValueError(f"Unsupported MQ Protocol: {base_config.mq_protocol}")
        
    client.connect()
    yield client
    client.disconnect()
