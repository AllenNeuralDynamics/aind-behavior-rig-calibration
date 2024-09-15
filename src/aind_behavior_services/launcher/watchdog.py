import subprocess
from logging import Logger
from os import PathLike
from pathlib import Path
from typing import Optional, TypeVar

from requests.exceptions import HTTPError

from aind_behavior_services.aind_services.data_mapper import AdsSession
from aind_behavior_services.aind_services.watchdog import Watchdog
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import format_datetime

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)


def post_run_hook_routine(
    watchdog: Watchdog,
    logger: Logger,
    session_schema: TSession,
    ads_session: AdsSession,
    remote_path: PathLike,
    session_directory: PathLike,
):
    if watchdog is None:
        raise ValueError("Watchdog object is not defined.")
    if logger is None:
        raise ValueError("Logger object is not defined.")

    if not watchdog.is_running():
        logger.warning("Watchdog service is not running. Attempting to start it.")

        try:
            watchdog.force_restart(kill_if_running=False)
        except subprocess.CalledProcessError as e:
            logger.error("Failed to start watchdog service. %s", e)
        else:
            if not watchdog.is_running():
                logger.error("Failed to start watchdog service.")
            else:
                logger.info("Watchdog service restarted successfully.")

    logger.info("Creating watchdog manifest config.")
    if remote_path is None:
        raise ValueError(
            "Remote path is not defined in the session schema. \
                A remote path must be used to create a watchdog manifest."
        )
    watchdog_manifest_config = watchdog.create_manifest_config(
        ads_session=ads_session,
        source=Path(session_directory),
        destination=Path(remote_path),
        processor_full_name=",".join([name for name in ads_session.experimenter_full_name]),
        session_name=session_schema.session_name,
    )

    _manifest_name = f"manifest_{session_schema.session_name if session_schema.session_name else format_datetime(session_schema.date)}.yaml"
    _manifest_path = watchdog.dump_manifest_config(
        watchdog_manifest_config, path=Path(watchdog.watched_dir) / _manifest_name
    )
    logger.info("Watchdog manifest config created successfully at %s.", _manifest_path)


def is_valid_instance(logger: Logger, watchdog: Optional[Watchdog] = None) -> bool:
    if watchdog is None:
        logger.info("Watchdog service is disabled. Skipping validation.")
        return False

    logger.info("Watchdog service is enabled.")

    is_running = True
    if not watchdog.is_running():
        is_running = False
        logger.warning(
            "Watchdog service is not running. \
                            After the session is over, \
                            the launcher will attempt to forcefully restart it"
        )

    if not watchdog.is_valid_project_name():
        is_running = False
        try:
            logger.warning("Watchdog project name is not valid.")
        except HTTPError as e:
            logger.error("Failed to fetch project names from endpoint. %s", e)

    return is_running
