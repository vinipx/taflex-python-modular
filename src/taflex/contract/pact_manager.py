from typing import Any, Dict, Optional
from pact import Pact
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class PactManager:
    """
    Manager for Pact Contract Testing.
    Handles setup, interaction definition, and verification of pacts.
    """
    def __init__(self, config: AppConfig):
        self.config = config
        self.pact = Pact(
            Consumer=config.pact_consumer,
            Provider=config.pact_provider,
            pact_dir=config.pact_dir,
        )

    def start_service(self):
        """Start the mock service."""
        logger.info(f"Starting Pact mock service for {self.config.pact_consumer}")
        self.pact.start_service()

    def stop_service(self):
        """Stop the mock service and verify interactions."""
        logger.info(f"Stopping Pact mock service and verifying interactions")
        self.pact.stop_service()

    def given(self, provider_state: str) -> "PactManager":
        """Set the provider state."""
        self.pact.given(provider_state)
        return self

    def upon_receiving(self, scenario: str) -> "PactManager":
        """Set the scenario description."""
        self.pact.upon_receiving(scenario)
        return self

    def with_request(self, method: str, path: str, body: Any = None, headers: Dict[str, str] = None, query: Any = None) -> "PactManager":
        """Define the expected request."""
        self.pact.with_request(method, path, body, headers, query)
        return self

    def will_respond_with(self, status: int, body: Any = None, headers: Dict[str, str] = None) -> "PactManager":
        """Define the expected response."""
        self.pact.will_respond_with(status, body, headers)
        return self

    def verify(self):
        """Verify that the interactions defined were executed correctly."""
        logger.info("Verifying Pact interactions")
        self.pact.verify()

    @property
    def uri(self) -> str:
        """Return the URI of the mock service."""
        return self.pact.uri
