from __future__ import annotations

import abc
import logging
from typing import TypeVar

from aind_behavior_services.launcher._service import IService
from aind_behavior_services.session import AindBehaviorSessionModel

logger = logging.getLogger(__name__)

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)


class DataTransferService(IService, abc.ABC):
    @abc.abstractmethod
    def transfer(self, *args, **kwargs) -> None:
        pass
