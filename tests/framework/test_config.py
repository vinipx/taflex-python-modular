import os
import pytest
from taflex.core.config.app_config import AppConfig

def test_app_config_default_values():
    """Verify default values are set correctly when no env vars are present."""
    # Temporarily remove relevant env vars
    keys = ["EXECUTION_MODE", "BROWSER", "TIMEOUT_MS", "ENVIRONMENT"]
    original_values = {key: os.environ.get(key) for key in keys}
    for key in keys:
        if key in os.environ:
            del os.environ[key]
            
    try:
        config = AppConfig()
        assert config.execution_mode == "web"
        assert config.browser == "chromium"
        assert config.timeout_ms == 30000
        assert config.environment == "qa"
    finally:
        # Restore env vars
        for key, value in original_values.items():
            if value is not None:
                os.environ[key] = value

def test_app_config_override_from_env():
    """Verify env vars correctly override default values."""
    os.environ["EXECUTION_MODE"] = "api"
    os.environ["BROWSER"] = "firefox"
    os.environ["TIMEOUT_MS"] = "15000"
    os.environ["ENVIRONMENT"] = "staging"
    
    try:
        config = AppConfig()
        assert config.execution_mode == "api"
        assert config.browser == "firefox"
        assert config.timeout_ms == 15000
        assert config.environment == "staging"
    finally:
        # Cleanup
        for key in ["EXECUTION_MODE", "BROWSER", "TIMEOUT_MS", "ENVIRONMENT"]:
            if key in os.environ:
                del os.environ[key]
