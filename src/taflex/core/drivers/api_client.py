from abc import ABC, abstractmethod
from typing import Any, Optional

class ApiClient(ABC):
    @abstractmethod
    def start(self) -> Any:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def get(self, url: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def post(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def put(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def patch(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> Any:
        pass

    @abstractmethod
    def delete(self, url: str, **kwargs) -> Any:
        pass
