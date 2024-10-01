import datetime
import logging
import os
import sys
from pathlib import Path
from typing import Optional, TypeVar

import aind_behavior_services.utils as utils

TLogger = TypeVar("TLogger", bound=logging.Logger)


def default_logger_builder(logger: TLogger, output_path: Optional[os.PathLike]) -> logging.Logger:
    logger.setLevel(logging.INFO)
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    utc_formatter = _TzFormatter(fmt, tz=datetime.timezone.utc)
    tz_formatter = _TzFormatter(fmt)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(tz_formatter)
    logger.addHandler(console_handler)

    if output_path is not None:
        file_handler = logging.FileHandler(Path(output_path), encoding="utf-8", mode="w")
        file_handler.setFormatter(utc_formatter)
        logger.addHandler(file_handler)
    return logger


def shutdown_logger(logger: TLogger) -> None:
    dispose_logger(logger)
    logging.shutdown()


def dispose_logger(logger: TLogger) -> TLogger:
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
    return logger


class _TzFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self._tz = kwargs.pop("tz", None)
        super().__init__(*args, **kwargs)

    def formatTime(self, record, datefmt=None) -> str:
        record_time = datetime.datetime.fromtimestamp(record.created, tz=self._tz)
        return utils.format_datetime(record_time)
