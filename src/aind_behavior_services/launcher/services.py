import logging
from typing import Optional, Self, TypeVar, Union

import aind_behavior_services.launcher.app_services as app_services
import aind_behavior_services.launcher.resource_monitor_service as resource_monitor_service
import aind_behavior_services.launcher.watchdog_service as watchdog_service

SupportedServices = Union[
    watchdog_service.WatchdogService, resource_monitor_service.ResourceMonitor, app_services.BonsaiApp
]
TService = TypeVar("TService", bound=SupportedServices)


class Services:
    _watchdog: Optional[watchdog_service.WatchdogService]
    _logger: Optional[logging.Logger]
    _resource_monitor: Optional[resource_monitor_service.ResourceMonitor]
    _app: Optional[app_services.BonsaiApp]

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        watchdog: Optional[watchdog_service.WatchdogService] = None,
        resource_monitor: Optional[resource_monitor_service.ResourceMonitor] = None,
        app: Optional[app_services.BonsaiApp] = None,
    ) -> None:
        self._logger = logger
        self._watchdog = watchdog
        self._resource_monitor = resource_monitor
        self._app = app
        if logger is not None:
            self._register_logger()

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
        self._register_logger()

    def register_logger(self, logger: logging.Logger) -> Self:
        # For symmetry with other register methods
        self.logger = logger
        return self

    @property
    def watchdog(self) -> Optional[watchdog_service.WatchdogService]:
        return self._watchdog

    def register_watchdog(self, watchdog: watchdog_service.WatchdogService) -> Self:
        if self._watchdog is not None:
            raise ValueError("Watchdog already registered")
        self._watchdog = self._register_service(watchdog)
        return self

    @property
    def resource_monitor(self) -> Optional[resource_monitor_service.ResourceMonitor]:
        return self._resource_monitor

    def register_resource_monitor(self, resource_monitor: resource_monitor_service.ResourceMonitor) -> Self:
        if self._resource_monitor is not None:
            raise ValueError("Resource manager already registered")
        self._resource_monitor = self._register_service(resource_monitor)
        return self

    @property
    def app(self) -> Optional[app_services.BonsaiApp]:
        return self._app

    def register_app(self, app: app_services.BonsaiApp) -> Self:
        if self._app is not None:
            raise ValueError("App already registered")
        self._app = self._register_service(app)
        return self

    def validate_service(self, obj: Optional[TService]) -> bool:
        if obj is None:
            raise ValueError("Service not set")
        return obj.validate()

    def _register_service(self, obj: TService, register_logger: bool = True) -> TService:
        if register_logger:
            obj.logger = self.logger
        return obj

    def _register_logger(self) -> None:
        for service in (self._watchdog, self._resource_monitor, self._app):
            if service is not None:
                service.logger = self.logger
