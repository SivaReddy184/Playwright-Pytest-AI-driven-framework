"""
logger.py  –  Centralised Python logging setup.
Every module gets a child logger via get_logger(__name__).
"""
import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

_log_filename = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Root formatter
_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# File handler  (DEBUG+)
_file_handler = logging.FileHandler("logs/test_run.log", mode="a", encoding="utf-8")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(_formatter)

# Console handler (INFO+)
_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(_formatter)

# Configure root logger once
logging.basicConfig(level=logging.DEBUG, handlers=[_file_handler, _console_handler])


def get_logger(name: str) -> logging.Logger:
    """Return a named child logger inheriting root configuration."""
    return logging.getLogger(name)
