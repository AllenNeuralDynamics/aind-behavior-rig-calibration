from typing import Protocol


class IService(Protocol):
    """A minimal interface to ensure that services have expected functionality."""

    def __init__(self, *args, **kwargs) -> None: ...

    def validate(self, *args, **kwargs) -> bool: ...
