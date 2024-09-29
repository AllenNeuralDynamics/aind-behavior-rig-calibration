import logging
from typing import Optional, Self, TypeVar, Union

import aind_behavior_services.launcher.resource_monitor_service as resource_monitor_service
import aind_behavior_services.launcher.watchdog_service as watchdog_service

SupportedServices = Union[watchdog_service.WatchdogService, resource_monitor_service.ResourceMonitor]
TService = TypeVar("TService", bound=SupportedServices)


class Services:
    _watchdog: Optional[watchdog_service.WatchdogService]
    _logger: Optional[logging.Logger]
    _resource_monitor: Optional[resource_monitor_service.ResourceMonitor]

    def __init__(self, logger: Optional[logging.Logger] = None):
        self._watchdog = None
        self._logger = logger
        self._resource_monitor = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            raise ValueError("Logger not set")
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        if self._logger is not None:
            raise ValueError("Logger already set")
        self._logger = logger

    @property
    def watchdog(self) -> Optional[watchdog_service.WatchdogService]:
        return self._watchdog

    def register_watchdog(self, watchdog: watchdog_service.WatchdogService) -> Self:
        if self._watchdog is not None:
            raise ValueError("Watchdog already registered")
        self._watchdog = watchdog
        return self

    @property
    def resource_monitor(self) -> Optional[resource_monitor_service.ResourceMonitor]:
        return self._resource_monitor

    def register_resource_monitor(self, resource_monitor: resource_monitor_service.ResourceMonitor) -> Self:
        if self._resource_monitor is not None:
            raise ValueError("Resource manager already registered")
        self._resource_monitor = resource_monitor
        return self

    def register(self, service: TService) -> Self:
        if isinstance(service, watchdog_service.WatchdogService):
            return self.register_watchdog(service)
        elif isinstance(service, resource_monitor_service.ResourceMonitor):
            return self.register_resource_monitor(service)
        else:
            raise ValueError(f"Unsupported service: {service}")

    def validate_service(self, obj: Optional[TService]) -> bool:
        if obj is None:
            raise ValueError("Service not set")
        return obj.validate()
