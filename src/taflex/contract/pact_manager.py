from typing import Any, Dict, List, Optional
from pact import Pact
from taflex.core.config.app_config import AppConfig
from taflex.core.utils.logger import get_logger

logger = get_logger(__name__)

class PactManager:
    """
    Manager for Pact Contract Testing.
    Handles setup, interaction definition, and verification of pacts.
    Compatible with both pact-python v2 and v3+.
    """
    def __init__(self, config: AppConfig):
        self.config = config
        self._is_v3 = False
        try:
            # Try v2 initialization first (it accepts pact_dir)
            self.pact = Pact(
                consumer=config.pact_consumer,
                provider=config.pact_provider,
                pact_dir=config.pact_dir,
            )
        except TypeError:
            # pact-python v3+ has different constructor (only consumer/provider)
            logger.info("Detected pact-python v3+, using new API")
            self._is_v3 = True
            self.pact = Pact(config.pact_consumer, config.pact_provider)
        
        self._server = None
        self._current_interaction = None
        self._pending_state = None

    def start_service(self):
        """
        Start the mock service.
        For v3, we use lazy starting when the URI is first accessed.
        """
        if not self._is_v3:
            logger.info(f"Starting Pact mock service for {self.config.pact_consumer}")
            self.pact.start_service()

    def _ensure_v3_started(self):
        """Ensure the v3 mock server is started."""
        if self._is_v3 and not self._server:
            logger.info(f"Starting Pact mock service (Lazy) for {self.config.pact_consumer}")
            self._server = self.pact.serve()
            self._server.__enter__()

    def stop_service(self):
        """Stop the mock service and verify interactions."""
        logger.info(f"Stopping Pact mock service and verifying interactions")
        if self._is_v3:
            if self._server:
                # __exit__ in v3 automatically verifies and raises MismatchesError if needed
                try:
                    self._server.__exit__(None, None, None)
                finally:
                    # Always try to write the pact file
                    self.pact.write_file(directory=self.config.pact_dir)
                    self._server = None
        else:
            self.pact.stop_service()

    def given(self, provider_state: str) -> "PactManager":
        """Set the provider state."""
        if self._is_v3:
            if self._server:
                logger.warning("Adding provider state to a running v3 mock server may not work as expected.")
            
            if self._current_interaction:
                self._current_interaction.given(provider_state)
            else:
                self._pending_state = provider_state
        else:
            self.pact.given(provider_state)
        return self

    def upon_receiving(self, scenario: str) -> "PactManager":
        """Set the scenario description."""
        if self._is_v3:
            if self._server:
                logger.warning("Adding interaction to a running v3 mock server may not work as expected.")
            
            self._current_interaction = self.pact.upon_receiving(scenario)
            if self._pending_state:
                self._current_interaction.given(self._pending_state)
                self._pending_state = None
        else:
            self.pact.upon_receiving(scenario)
        return self

    def with_request(self, method: str, path: str, body: Any = None, headers: Dict[str, str] = None, query: Any = None) -> "PactManager":
        """Define the expected request."""
        if self._is_v3:
            if not self._current_interaction:
                self.upon_receiving("Default Interaction")
            
            self._current_interaction.with_request(method, path)
            if body:
                self._current_interaction.with_body(body, part='Request')
            if headers:
                self._current_interaction.with_headers(headers, part='Request')
            if query:
                if isinstance(query, dict):
                    self._current_interaction.with_query_parameters(query)
                else:
                    self._current_interaction.with_query_parameter(str(query))
        else:
            self.pact.with_request(method, path, body, headers, query)
        return self

    def will_respond_with(self, status: int, body: Any = None, headers: Dict[str, str] = None) -> "PactManager":
        """Define the expected response."""
        if self._is_v3:
            if not self._current_interaction:
                raise RuntimeError("Interaction must be initialized with upon_receiving or with_request first.")
            
            self._current_interaction.will_respond_with(status)
            if body:
                self._current_interaction.with_body(body, part='Response')
            if headers:
                self._current_interaction.with_headers(headers, part='Response')
        else:
            self.pact.will_respond_with(status, body, headers)
        return self

    def verify(self):
        """Verify that the interactions defined were executed correctly."""
        if not self._is_v3:
            logger.info("Verifying Pact interactions")
            self.pact.verify()

    @property
    def uri(self) -> str:
        """Return the URI of the mock service."""
        if self._is_v3:
            self._ensure_v3_started()
            return str(self._server.url) if self._server else ""
        return self.pact.uri
