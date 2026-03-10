from abc import ABC, abstractmethod
from typing import Any, Callable, Optional


class BaseMQClient(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def publish(self, destination: str, payload: Any, headers: Optional[dict] = None):
        """Inject a message into a queue or topic."""
        pass

    @abstractmethod
    def wait_for_message(self, destination: str, timeout: int, condition: Callable[[Any], bool]) -> Any:
        """
        Poll or block on a queue until a message matching the condition arrives.
        Should raise TimeoutError if not found.
        """
        pass
    
    @abstractmethod
    def purge_queue(self, destination: str):
        """Clear out existing messages before a test starts."""
        pass
