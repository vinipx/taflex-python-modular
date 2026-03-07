import pytest

def pytest_configure(config):
    # Dynamically detect modules
    config.addinivalue_line("markers", "api: mark test as api test")
    config.addinivalue_line("markers", "web: mark test as web test")
    config.addinivalue_line("markers", "mobile: mark test as mobile test")

    # Load ReportPortal settings from AppConfig if not already set in CLI/ini
    from taflex.core.config.app_config import AppConfig
    app_config = AppConfig()

    # Map AppConfig/ENV variables to pytest-reportportal internal config names
    rp_mapping = {
        "rp_endpoint": app_config.rp_endpoint,
        "rp_api_key": app_config.rp_api_key or app_config.rp_uuid,
        "rp_project": app_config.rp_project,
        "rp_launch": app_config.rp_launch,
    }

    if "reportportal" in app_config.reporters:
        config.option.rp_enabled = True
        for key, value in rp_mapping.items():
            if value and not config.getoption(key, default=None):
                config.option.__dict__[key] = value

    if "xray" in app_config.reporters:
        config.option.jira_xray = True

@pytest.fixture
def web_driver():
    from taflex.core.drivers.driver_factory import DriverFactory
    from taflex.core.config.app_config import AppConfig
    config = AppConfig().model_copy(update={'execution_mode': 'web'})
    driver_instance = DriverFactory.create(config)
    driver_instance.start()
    yield driver_instance
    driver_instance.stop()

@pytest.fixture
def api_driver():
    from taflex.core.drivers.driver_factory import DriverFactory
    from taflex.core.config.app_config import AppConfig
    config = AppConfig().model_copy(update={'execution_mode': 'api'})
    driver_instance = DriverFactory.create(config)
    driver_instance.start()
    yield driver_instance
    driver_instance.stop()

@pytest.fixture
def mobile_driver():
    from taflex.core.drivers.driver_factory import DriverFactory
    from taflex.core.config.app_config import AppConfig
    config = AppConfig().model_copy(update={'execution_mode': 'mobile'})
    driver_instance = DriverFactory.create(config)
    driver_instance.start()
    yield driver_instance
    driver_instance.stop()

@pytest.fixture
def driver(request):
    from taflex.core.drivers.driver_factory import DriverFactory
    from taflex.core.config.app_config import AppConfig
    
    config = AppConfig()
    
    # Override execution_mode if marker is present
    if request.node.get_closest_marker("api"):
        config.execution_mode = "api"
    elif request.node.get_closest_marker("web"):
        config.execution_mode = "web"
    elif request.node.get_closest_marker("mobile"):
        config.execution_mode = "mobile"
    
    # Create the correct driver based on EXECUTION_MODE in .env or marker override
    driver_instance = DriverFactory.create(config)
    
    # Start driver (launches browser, or init API client, or starts Appium)
    driver_instance.start()
    
    yield driver_instance
    
    # Teardown
    driver_instance.stop()
