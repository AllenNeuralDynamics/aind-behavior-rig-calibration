from __future__ import annotations

import abc
import datetime
import json
import logging
import os
import subprocess
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, TypeVar

import pydantic
import requests
import yaml
from aind_data_schema.core.session import Session as AdsSession
from aind_data_schema_models.platforms import Platform
from aind_watchdog_service.models.manifest_config import BucketType, ManifestConfig
from aind_watchdog_service.models.watch_config import WatchConfig
from pydantic import BaseModel
from requests.exceptions import HTTPError

from aind_behavior_services.launcher._service import IService
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import format_datetime

logger = logging.getLogger(__name__)

TSession = TypeVar("TSession", bound=AindBehaviorSessionModel)


class DataTransferService(IService, abc.ABC):
    @abc.abstractmethod
    def transfer(self, *args, **kwargs) -> None:
        pass


class WatchdogDataTransferService(DataTransferService):
    try:
        import aind_watchdog_service
    except ImportError as e:
        e.add_note(
            "The 'aind-watchdog-service' package is required to use this module. \
                Install the optional dependencies defined in `project.toml' \
                    by running `pip install .[aind-services]`"
        )
        raise

    DEFAULT_EXE: Optional[str] = os.getenv("WATCHDOG_EXE", None)
    DEFAULT_CONFIG: Optional[str] = os.getenv("WATCHDOG_CONFIG", None)

    def __init__(
        self,
        destination: PathLike,
        schedule_time: Optional[datetime.time] = datetime.time(hour=20),
        project_name: Optional[str] = None,
        platform: Platform = getattr(Platform, "BEHAVIOR"),
        capsule_id: Optional[str] = None,
        script: Optional[Dict[str, List[str]]] = None,
        s3_bucket: BucketType = BucketType.PRIVATE,
        mount: Optional[str] = None,
        force_cloud_sync: bool = True,
        transfer_endpoint: str = "http://aind-data-transfer-service/api/v1/submit_jobs",
        validate: bool = True,
    ) -> None:
        self.destination = destination
        self.project_name = project_name
        self.schedule_time = schedule_time
        self.platform = platform
        self.capsule_id = capsule_id
        self.script = script
        self.s3_bucket = s3_bucket
        self.mount = mount
        self.force_cloud_sync = force_cloud_sync
        self.transfer_endpoint = transfer_endpoint

        if self.DEFAULT_EXE is None or self.DEFAULT_CONFIG is None:
            raise ValueError("WATCHDOG_EXE and WATCHDOG_CONFIG environment variables must be defined.")

        self.executable_path = Path(self.DEFAULT_EXE)
        self.config_path = Path(self.DEFAULT_CONFIG)
        self._config_model: WatchConfig = None
        if validate:
            self.validate(create_config=True)

    def transfer(self, *args, **kwargs) -> None:
        self.create_manifest_from_ads_session(*args, **kwargs)

    def validate(self, create_config: bool = True) -> bool:
        logger.info("Attempting to validate Watchdog service.")
        if not self.executable_path.exists():
            raise FileNotFoundError(f"Executable not found at {self.executable_path}")
        if not self.config_path.exists():
            if not create_config:
                raise FileNotFoundError(f"Config file not found at {self.config_path}")
            else:
                self._config_model = self.create_watchdog_config(
                    self.config_path.parent / "Manifests", self.config_path.parent / "Completed"
                )
                self._write_yaml(self._config_model, self.config_path)
        else:
            self._config_model = WatchConfig.model_validate(self._read_yaml(self.config_path))

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

    @staticmethod
    def create_watchdog_config(
        watched_directory: os.PathLike,
        manifest_complete_directory: os.PathLike,
        webhook_url: Optional[str] = None,
        create_dir: bool = True,
    ) -> WatchConfig:
        """Create a WatchConfig object"""

        if create_dir:
            if not Path(watched_directory).exists():
                Path(watched_directory).mkdir(parents=True, exist_ok=True)
            if not Path(manifest_complete_directory).exists():
                Path(manifest_complete_directory).mkdir(parents=True, exist_ok=True)

        return WatchConfig(
            flag_dir=str(watched_directory),
            manifest_complete=str(manifest_complete_directory),
            webhook_url=webhook_url,
        )

    def is_valid_project_name(self) -> bool:
        project_names = self._get_project_names()
        return self.project_name in project_names

    def create_manifest_config(
        self,
        source: os.PathLike,
        ads_session: AdsSession,
        ads_schemas: Optional[List[os.PathLike]] = None,
        session_name: Optional[str] = None,
        **kwargs,
    ) -> ManifestConfig:
        """Create a ManifestConfig object"""
        project_name = kwargs.pop("project_name", self.project_name)
        schedule_time = kwargs.pop("schedule_time", self.schedule_time)
        platform = kwargs.pop("platform", self.platform)
        capsule_id = kwargs.pop("capsule_id", self.capsule_id)
        script = kwargs.pop("script", self.script)
        s3_bucket = kwargs.pop("s3_bucket", self.s3_bucket)
        mount = kwargs.pop("mount", self.mount)
        force_cloud_sync = kwargs.pop("force_cloud_sync", self.force_cloud_sync)
        transfer_endpoint = kwargs.pop("transfer_endpoint", self.transfer_endpoint)
        validate_project_name = kwargs.pop("validate_project_name", True)
        processor_full_name = (
            kwargs.pop("processor_full_name", None)
            or ",".join(ads_session.experimenter_full_name)
            or os.environ.get("USERNAME", "unknown")
        )

        destination = Path(self.destination).resolve()
        source = Path(source).resolve()

        if session_name is None:
            session_name = (ads_session.stimulus_epochs[0]).stimulus_name

        if validate_project_name:
            project_names = self._get_project_names()
            if project_name not in project_names:
                raise ValueError(f"Project name {project_name} not found in {project_names}")

        ads_schemas = [source / "session.json"] if ads_schemas is None else ads_schemas

        return ManifestConfig(
            name=session_name,
            modalities={
                str(modality.abbreviation): [str(path.resolve()) for path in [source / str(modality.abbreviation)]]
                for modality in ads_session.data_streams[0].stream_modalities
            },
            subject_id=int(ads_session.subject_id),
            acquisition_datetime=ads_session.session_start_time,
            schemas=[str(value) for value in ads_schemas],
            destination=str(destination.resolve()),
            mount=mount,
            processor_full_name=processor_full_name,
            project_name=project_name,
            schedule_time=schedule_time,
            platform=getattr(platform, "abbreviation"),
            capsule_id=capsule_id,
            s3_bucket=s3_bucket,
            script=script if script else {},
            force_cloud_sync=force_cloud_sync,
            transfer_endpoint=transfer_endpoint,
        )

    @staticmethod
    def _get_project_names(
        end_point: str = "http://aind-metadata-service/project_names", timeout: int = 5
    ) -> list[str]:
        response = requests.get(end_point, timeout=timeout)
        if response.ok:
            content = json.loads(response.content)
        else:
            response.raise_for_status()
        return content["data"]

    def is_running(self) -> bool:
        output = subprocess.check_output(
            ["tasklist", "/FI", f"IMAGENAME eq {self.executable_path.name}"], shell=True, encoding="utf-8"
        )
        processes = [line.split()[0] for line in output.splitlines()[3:]]
        return len(processes) > 0

    def force_restart(self, kill_if_running: bool = True) -> subprocess.Popen[bytes]:
        if kill_if_running is True:
            while self.is_running():
                subprocess.run(["taskkill", "/IM", self.executable_path.name, "/F"], shell=True, check=True)

        cmd_builder = "{exe} -c {config}".format(exe=self.executable_path, config=self.config_path)

        return subprocess.Popen(cmd_builder, start_new_session=True, shell=True)

    def dump_manifest_config(
        self, manifest_config: ManifestConfig, path: Optional[os.PathLike] = None, make_dir: bool = True
    ) -> Path:
        path = Path(path if path else self._config_model.flag_dir / f"manifest_{manifest_config.name}.yaml").resolve()
        if "manifest" not in path.name:
            raise ValueError("The file name must contain the string 'manifest' for the watchdog to work.")
        if make_dir and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        manifest_config.destination = str(Path.as_posix(Path(manifest_config.destination)))
        manifest_config.schemas = [str(Path.as_posix(Path(schema))) for schema in manifest_config.schemas]
        for modality in manifest_config.modalities:
            manifest_config.modalities[modality] = [
                str(Path.as_posix(Path(_path))) for _path in manifest_config.modalities[modality]
            ]

        self._write_yaml(manifest_config, path)
        return path

    @staticmethod
    def _yaml_dump(model: BaseModel) -> str:
        native_json = json.loads(model.model_dump_json())
        return yaml.dump(native_json, default_flow_style=False)

    @classmethod
    def _write_yaml(cls, model: BaseModel, path: PathLike) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(cls._yaml_dump(model))

    @staticmethod
    def _read_yaml(path: PathLike) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def create_manifest_from_ads_session(
        self,
        session_schema: TSession,
        ads_session: AdsSession,
        session_directory: PathLike,
    ):
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
            if self.destination is None:
                raise ValueError("Remote path must be provided.")

            watchdog_manifest_config = self.create_manifest_config(
                ads_session=ads_session,
                source=Path(session_directory),
                destination=Path(self.destination),
                processor_full_name=",".join([name for name in ads_session.experimenter_full_name]),
                session_name=session_schema.session_name,
            )

            _manifest_name = f"manifest_{session_schema.session_name if session_schema.session_name else format_datetime(session_schema.date)}.yaml"
            _manifest_path = self.dump_manifest_config(
                watchdog_manifest_config, path=Path(self._config_model.flag_dir) / _manifest_name
            )
            logger.info("Watchdog manifest config created successfully at %s.", _manifest_path)

        except (pydantic.ValidationError, ValueError, IOError) as e:
            logger.error("Failed to create watchdog manifest config. %s", e)
