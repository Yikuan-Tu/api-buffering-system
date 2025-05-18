import logging
import sys
from typing import Optional
from app.utils.config import LOG_LEVEL

def setup_logging(log_level: Optional[str] = None):
    if not log_level:
        log_level = LOG_LEVEL
    
    try:
        level = getattr(logging, log_level)
    except AttributeError:
        level = logging.INFO # Set default to INFO
        logging.warning(f"Invalid LOG_LEVEL '{log_level}'. Defaulting to INFO")

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set SQLite logging to WARNING to avoid verbose output
    logging.getLogger('sqlite3').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)
