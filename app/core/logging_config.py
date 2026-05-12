import logging
from logging import Handler, LogRecord
from collections import deque
from logging.handlers import RotatingFileHandler
from pathlib import Path

class InMemoryLogHandler(Handler):
    def __init__(self, capacity: int = 200) -> None:
        super().__init__()
        self.records: deque[str] = deque(maxlen=capacity)

    def emit(self, record: LogRecord) -> None:
        try:
            self.records.append(self.format(record))
        except Exception:
            self.handleError(record)

in_memory_handler = InMemoryLogHandler(capacity=200)

def configure_logging() -> None:
    Path("logs").mkdir(exist_ok=True)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    in_memory_handler.setFormatter(formatter)
    in_memory_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(in_memory_handler)