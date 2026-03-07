from taflex.core.config.app_config import AppConfig

class DriverFactory:
    @staticmethod
    def create(config: AppConfig):
        if config.execution_mode == 'web':
            from taflex.web.driver import PlaywrightDriver
            return PlaywrightDriver(config)
        elif config.execution_mode == 'api':
            from taflex.api.client import HttpxClient
            return HttpxClient(config)
        elif config.execution_mode == 'mobile':
            from taflex.mobile.driver import AppiumDriver
            return AppiumDriver(config)
        else:
            raise ValueError(f"Unsupported execution mode: {config.execution_mode}")
