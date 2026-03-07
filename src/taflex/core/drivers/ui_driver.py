from abc import ABC, abstractmethod
from typing import Any, Optional

class UiDriver(ABC):
    @abstractmethod
    def start(self) -> Any:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def navigate(self, url: str) -> None:
        pass

    @abstractmethod
    def click(self, selector: str) -> None:
        pass

    @abstractmethod
    def type(self, selector: str, text: str) -> None:
        pass

    @abstractmethod
    def get_text(self, selector: str) -> str:
        pass

    @abstractmethod
    def is_visible(self, selector: str) -> bool:
        pass

    @abstractmethod
    def wait_for_selector(self, selector: str, timeout_ms: Optional[int] = None) -> Any:
        pass

    @abstractmethod
    def screenshot(self, path: str) -> None:
        pass
