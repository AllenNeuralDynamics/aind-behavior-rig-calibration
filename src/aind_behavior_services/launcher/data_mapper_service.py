import logging
from typing import Optional, TypeVar

from aind_behavior_services.aind_services.data_mapper import AdsSession, map_from_session_root
from aind_behavior_services.launcher._service import IService
from aind_behavior_services.session import AindBehaviorSessionModel

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)


class DataMapperService(IService):
    def __init__(self, *args, logger: Optional[logging.Logger] = None, **kwargs):
        self._logger = logger

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            raise ValueError("Logger not set")
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger) -> None:
        if self._logger is not None:
            raise ValueError("Logger already set")
        self._logger = logger

    def validate(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class AindDataSchemaSessionDataMapper(DataMapperService):
    def validate(self, *args, **kwargs) -> bool:
        return True

    def map_from_session_root(self, *args, **kwargs) -> AdsSession:
        self.logger.info("Mapping to aind-data-schema Session")
        return map_from_session_root(*args, **kwargs)
