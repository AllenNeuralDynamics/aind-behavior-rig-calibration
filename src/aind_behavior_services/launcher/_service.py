import logging
from typing import Optional, Protocol


class IService(Protocol):
    """A minimal interface to ensure that services have expected functionality."""

    def __init__(self, logger: Optional[logging.Logger], *args, **kwargs) -> None: ...

    def validate(self, *args, **kwargs) -> bool: ...

    @property
    def logger(self) -> Optional[logging.Logger]: ...
