
"""
Logging configuration utilities.
"""
import logging

def setup_logging(level: str = 'INFO') -> None:
    """Configure application logging.

    Args:
        level: Logging level name (e.g., "DEBUG", "INFO", "WARNING").
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
    )
