from functools import lru_cache
import inspect
import logging
import sys

from loguru import logger as _logger


@lru_cache(1)
def init_logger():
    _logger.remove()
    _logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{name}</level> | "
            "<level>{level}</level> | "
            "<level>{message}</level>"
        ),
        backtrace=False,
        diagnose=False,
        enqueue=True,
        colorize=True,
    )
    return _logger


logger = init_logger()


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


__all__ = (
    "logger",
    "InterceptHandler",
)
