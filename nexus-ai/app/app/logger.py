"""
Logging configuration for Nexus AI
"""
import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("nexus_ai")
logger.setLevel(logging.INFO)

# Console handler (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(console_formatter)

# File handler (logs to file)
file_handler = logging.FileHandler(LOGS_DIR / "nexus_ai.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
file_handler.setFormatter(file_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent propagation to root logger
logger.propagate = False


def get_logger(name: str = "nexus_ai") -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
