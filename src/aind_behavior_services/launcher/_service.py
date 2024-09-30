import logging
from typing import Optional, Protocol


class IService(Protocol):
    """A minimal interface to ensure that services have expected functionality."""

    def __init__(self, *args, logger: Optional[logging.Logger] = None, **kwargs) -> None: ...

    def validate(self, *args, **kwargs) -> bool: ...

    @property
    def logger(self) -> logging.Logger: ...

    @logger.setter
    def logger(self, logger: logging.Logger) -> None: ...
