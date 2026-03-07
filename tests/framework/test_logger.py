from taflex.core.utils.logger import get_logger
import logging

def test_get_logger():
    """Verify get_logger returns a logging.Logger instance with the correct name."""
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
