import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


def get_env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} not set")
    return value


DB_PATH = Path(get_env("DB_PATH", "/data/database.db"))
BUFFER_SIZE = int(get_env("BUFFER_SIZE", "100"))
LOG_LEVEL = get_env("LOG_LEVEL", "INFO").upper()
# # Ensure data directory exists
# DB_PATH.parent.mkdir(parents=True, exist_ok=True)
