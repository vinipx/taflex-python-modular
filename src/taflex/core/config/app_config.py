from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AppConfig(BaseSettings):
    # Core settings
    execution_mode: str = "web"
    environment: str = "qa"
    base_url: Optional[str] = None
    reporters: str = ""
    
    # Web settings
    browser: str = "chromium"
    headless: bool = True
    timeout_ms: int = 30000

    # Mobile settings
    appium_server_url: str = "http://localhost:4723/wd/hub"
    platform_name: str = "Android"
    device_name: Optional[str] = None

    # ReportPortal settings
    rp_endpoint: Optional[str] = None
    rp_uuid: Optional[str] = None
    rp_api_key: Optional[str] = None
    rp_project: Optional[str] = None
    rp_launch: Optional[str] = None

    # Jira Xray settings
    xray_client_id: Optional[str] = None
    xray_client_secret: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
