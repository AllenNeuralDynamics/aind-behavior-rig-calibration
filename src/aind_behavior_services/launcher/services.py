import logging
from typing import Optional, Self, TypeVar, Union

import aind_behavior_services.launcher.app_service as app_service
import aind_behavior_services.launcher.resource_monitor_service as resource_monitor_service
import aind_behavior_services.launcher.watchdog_service as watchdog_service
from aind_behavior_services.launcher.data_mapper_service import AindDataSchemaSessionDataMapper

logger = logging.getLogger(__name__)

SupportedServices = Union[
    watchdog_service.WatchdogService,
    resource_monitor_service.ResourceMonitor,
    app_service.BonsaiApp,
    AindDataSchemaSessionDataMapper,
]

TService = TypeVar("TService", bound=SupportedServices)


class Services:
    # todo: This could use some future refactoring to make it more generic. For instance, not subclassing App
    _watchdog: Optional[watchdog_service.WatchdogService]
    _resource_monitor: Optional[resource_monitor_service.ResourceMonitor]
    _app: Optional[app_service.BonsaiApp]
    _data_mapper: Optional[AindDataSchemaSessionDataMapper]

    def __init__(
        self,
        *args,
        watchdog: Optional[watchdog_service.WatchdogService] = None,
        resource_monitor: Optional[resource_monitor_service.ResourceMonitor] = None,
        app: Optional[app_service.BonsaiApp] = None,
        data_mapper: Optional[AindDataSchemaSessionDataMapper] = None,
        **kwargs,
    ) -> None:
        self._watchdog = watchdog
        self._resource_monitor = resource_monitor
        self._app = app
        self._data_mapper = data_mapper

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

    @property
    def app(self) -> Optional[app_service.BonsaiApp]:
        return self._app

    def register_app(self, app: app_service.BonsaiApp) -> Self:
        if self._app is not None:
            raise ValueError("App already registered")
        self._app = app
        return self

    @property
    def data_mapper(self) -> Optional[AindDataSchemaSessionDataMapper]:
        return self._data_mapper

    def register_data_mapper(self, data_mapper: AindDataSchemaSessionDataMapper) -> Self:
        if self._data_mapper is not None:
            raise ValueError("Data mapper already registered")
        self._data_mapper = data_mapper
        return self

    def validate_service(self, obj: Optional[TService]) -> bool:
        if obj is None:
            raise ValueError("Service not set")
        return obj.validate()
