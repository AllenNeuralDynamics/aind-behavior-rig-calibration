import logging
from typing import Protocol


class Service(Protocol):
    def validate(self, logger: logging.Logger, *args, **kwargs) -> bool: ...

    def register(self, *args, **kwargs) -> None: ...
