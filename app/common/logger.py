import logging
import os
import sys
from datetime import datetime
from typing import Optional

# Directory to store log files
LOGS_DIR = os.getenv("LOGS_DIR", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate timestamped log filename
LOG_FILE_NAME = f"app-{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE_NAME)

# Log formatting template
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default log level from environment or INFO
DEFAULT_LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
DEFAULT_LOG_LEVEL = getattr(logging, DEFAULT_LOG_LEVEL_STR, logging.INFO)


def setup_logging(
    log_file: Optional[str] = LOG_FILE_PATH,
    level: int = DEFAULT_LOG_LEVEL,
    log_to_console: bool = True
) -> None:
    """
    Configures root logger with file and console handlers.
    """
    handlers: list[logging.Handler] = []

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        handlers.append(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        handlers.append(console_handler)

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True
    )


# Run default logging setup on import
setup_logging()


def get_logger(name: str = "app") -> logging.Logger:
    """
    Retrieves a configured logger instance by module/component name.

    Args:
        name (str): Name of the module or component requesting the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)