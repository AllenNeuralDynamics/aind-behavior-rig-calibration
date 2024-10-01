import logging
import subprocess
from os import PathLike
from pathlib import Path
from typing import Optional, TypeVar

import pydantic
from requests.exceptions import HTTPError

import aind_behavior_services.aind_services.watchdog as watchdog
from aind_behavior_services.aind_services.data_mapper import AdsSession
from aind_behavior_services.launcher._service import IService
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import format_datetime

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)


class WatchdogService(watchdog.Watchdog, IService):
    def __init__(self, *args, logger: Optional[logging.Logger] = None, **kwargs):
        super().__init__(*args, **kwargs)
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

    def create_manifest_from_ads_session(
        self,
        session_schema: TSession,
        ads_session: AdsSession,
        remote_path: PathLike,
        session_directory: PathLike,
    ):
        logger = self.logger
        try:
            if not self.is_running():
                logger.warning("Watchdog service is not running. Attempting to start it.")

                try:
                    self.force_restart(kill_if_running=False)
                except subprocess.CalledProcessError as e:
                    logger.error("Failed to start watchdog service. %s", e)
                else:
                    if not self.is_running():
                        logger.error("Failed to start watchdog service.")
                    else:
                        logger.info("Watchdog service restarted successfully.")

            logger.info("Creating watchdog manifest config.")
            if remote_path is None:
                raise ValueError(
                    "Remote path is not defined in the session schema. \
                        A remote path must be used to create a watchdog manifest."
                )
            watchdog_manifest_config = self.create_manifest_config(
                ads_session=ads_session,
                source=Path(session_directory),
                destination=Path(remote_path),
                processor_full_name=",".join([name for name in ads_session.experimenter_full_name]),
                session_name=session_schema.session_name,
            )

            _manifest_name = f"manifest_{session_schema.session_name if session_schema.session_name else format_datetime(session_schema.date)}.yaml"
            _manifest_path = self.dump_manifest_config(
                watchdog_manifest_config, path=Path(self.watched_dir) / _manifest_name
            )
            logger.info("Watchdog manifest config created successfully at %s.", _manifest_path)

        except (pydantic.ValidationError, ValueError, IOError) as e:
            logger.error("Failed to create watchdog manifest config. %s", e)

    def validate(self, *args, **kwargs) -> bool:
        logger = self.logger
        logger.info("Watchdog service is enabled.")
        is_running = True
        if not self.is_running():
            is_running = False
            logger.warning(
                "Watchdog service is not running. \
                                After the session is over, \
                                the launcher will attempt to forcefully restart it"
            )

        if not self.is_valid_project_name():
            is_running = False
            try:
                logger.warning("Watchdog project name is not valid.")
            except HTTPError as e:
                logger.error("Failed to fetch project names from endpoint. %s", e)

        return is_running
