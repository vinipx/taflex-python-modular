import pytest
from pydantic import ValidationError
from taflex.core.config.app_config import AppConfig

def test_app_config_default_values(monkeypatch):
    """Verify default values are set correctly when no env vars are present."""
    # Temporarily remove relevant env vars using monkeypatch
    keys = ["EXECUTION_MODE", "BROWSER", "TIMEOUT_MS", "ENVIRONMENT"]
    for key in keys:
        monkeypatch.delenv(key, raising=False)
            
    config = AppConfig()
    assert config.execution_mode == "web"
    assert config.browser == "chromium"
    assert config.timeout_ms == 30000
    assert config.environment == "qa"

def test_app_config_invalid_type_from_env(monkeypatch):
    """Verify that invalid data types in env vars raise a validation error."""
    monkeypatch.setenv("TIMEOUT_MS", "not_a_number")
    with pytest.raises(ValidationError):
        AppConfig()

def test_app_config_extra_env_vars_ignored(monkeypatch):
    """Verify that extra environment variables do not affect the config object."""
    monkeypatch.setenv("TAFLEX_UNKNOWN_FIELD", "some_value")
    config = AppConfig()
    assert not hasattr(config, "taflex_unknown_field")

def test_app_config_boolean_parsing(monkeypatch):
    """Verify that boolean strings are correctly parsed from env vars."""
    monkeypatch.setenv("HEADLESS", "false")
    config = AppConfig()
    assert config.headless is False
    
    monkeypatch.setenv("HEADLESS", "true")
    config = AppConfig()
    assert config.headless is True
