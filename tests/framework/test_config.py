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

def test_app_config_invalid_type_from_env():
    """Verify that invalid data types in env vars raise a validation error."""
    os.environ["TIMEOUT_MS"] = "not_a_number"
    try:
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            AppConfig()
    finally:
        if "TIMEOUT_MS" in os.environ:
            del os.environ["TIMEOUT_MS"]

def test_app_config_extra_env_vars_ignored():
    """Verify that extra environment variables do not affect the config object."""
    os.environ["TAFLEX_UNKNOWN_FIELD"] = "some_value"
    try:
        config = AppConfig()
        assert not hasattr(config, "taflex_unknown_field")
    finally:
        if "TAFLEX_UNKNOWN_FIELD" in os.environ:
            del os.environ["TAFLEX_UNKNOWN_FIELD"]

def test_app_config_boolean_parsing():
    """Verify that boolean strings are correctly parsed from env vars."""
    os.environ["HEADLESS"] = "false"
    try:
        config = AppConfig()
        assert config.headless is False
        
        os.environ["HEADLESS"] = "true"
        config = AppConfig()
        assert config.headless is True
    finally:
        if "HEADLESS" in os.environ:
            del os.environ["HEADLESS"]
