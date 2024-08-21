try:
    import aind_watchdog_service  # noqa: F401
except ImportError as e:
    e.add_note(
        "The 'aind-watchdog-service' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-extra-services]`"
    )
    raise

import datetime
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml
from aind_data_schema.core.session import Session
from aind_data_schema_models.platforms import Platform
from aind_watchdog_service.models.manifest_config import BucketType, ManifestConfig
from aind_watchdog_service.models.watch_config import WatchConfig

from aind_behavior_services.session import AindBehaviorSessionModel

DEFAULT_WATCHED_DIRECTORY = Path((os.getenv("LOCALAPPDATA") or ".") + "aind-watchdog-service").resolve()


class Watchdog:
    def __init__(
        self,
        project_name: str,
        time_to_run: Optional[datetime.time] = datetime.time(hour=20),
        watched_folder: os.PathLike = DEFAULT_WATCHED_DIRECTORY,
    ) -> None:
        self.project_name = project_name
        self.schedule_time = time_to_run
        self.watched_folder = Path(watched_folder)

    @staticmethod
    def create_watchdog_config(
        watched_directory: Optional[os.PathLike],
        manifest_complete_directory: Optional[os.PathLike],
        webhook_url: Optional[str] = None,
    ) -> WatchConfig:
        """Create a WatchConfig object"""
        return WatchConfig(
            flag_dir=str(watched_directory),
            manifest_complete=str(manifest_complete_directory),
            webhook_url=webhook_url,
        )

    def validate_project_name(self) -> bool:
        project_names = Watchdog._get_project_names()
        return self.project_name in project_names

    @staticmethod
    def create_manifest_config(
        session: Session,
        source: os.PathLike,
        destination: os.PathLike,
        *args,
        project_name: str,
        session_name: Optional[str] = None,
        processor_full_name: Optional[str] = None,
        schedule_time: Optional[
            datetime.time
        ] = None,  # TODO https://github.com/AllenNeuralDynamics/aind-watchdog-service/pull/37
        platform: Platform = getattr(Platform, "BEHAVIOR"),
        capsule_id: Optional[str] = None,
        script: Optional[Dict[str, List[str]]] = None,
        s3_bucket: BucketType = BucketType.PRIVATE,
        mount: Optional[str] = None,
        validate_project_name: bool = True,
    ) -> ManifestConfig:
        """Create a ManifestConfig object"""
        processor_full_name = processor_full_name or os.environ.get("USERNAME", "unknown")

        destination = Path(destination).resolve()
        source = Path(source).resolve()

        if session_name is None:
            session_name = (session.stimulus_epochs[0]).stimulus_name

        if validate_project_name:
            project_names = Watchdog._get_project_names()
            if project_name not in project_names:
                raise ValueError(f"Project name {project_name} not found in {project_names}")

        return ManifestConfig(
            name=session_name,
            modalities={
                str(modality.abbreviation): [str(path.resolve()) for path in [source / str(modality.abbreviation)]]
                for modality in session.data_streams[0].stream_modalities
            },
            subject_id=int(session.subject_id),
            acquisition_datetime=session.session_start_time,
            schemas=[str(path.resolve()) for path in [source / "session.json", source / "other"]],
            destination=str(destination.resolve()),
            mount=mount,
            processor_full_name=processor_full_name,
            project_name=project_name,
            schedule_time=schedule_time,
            platform=getattr(platform, "abbreviation"),
            capsule_id=capsule_id,
            s3_bucket=s3_bucket,
            script=script if script else {},
        )

    @staticmethod
    def _get_project_names(
        end_point: str = "http://aind-metadata-service/project_names", timeout: int = 5
    ) -> list[str]:
        response = requests.get(end_point, timeout=timeout)
        if response.ok:
            jData = json.loads(response.content)
        else:
            response.raise_for_status()
        return jData["data"]

    def create_manifest_config_from_session(
        self,
        session: AindBehaviorSessionModel,
        aind_data_schema_session: Session,
        project_name: Optional[str] = None,
        schedule_time: Optional[datetime.time] = None,
        platform: Platform = getattr(Platform, "BEHAVIOR"),
        **kwargs,
    ) -> ManifestConfig:
        if session.remote_path is None:
            raise ValueError(
                "Remote path is not defined in the session schema. \
                    A remote path must be used to create a watchdog manifest."
            )

        if project_name is None:
            project_name = self.project_name

        if schedule_time is None:
            schedule_time = self.schedule_time  # if neither is provided, the watchdog will run immediately

        return Watchdog.create_manifest_config(
            session=aind_data_schema_session,
            source=Path(session.root_path),
            destination=Path(session.remote_path),
            project_name=project_name,
            processor_full_name=",".join([name for name in aind_data_schema_session.experimenter_full_name]),
            schedule_time=schedule_time,
            platform=platform,
            **kwargs,
        )

    @staticmethod
    def is_running(process_name: str = "watchdog.exe") -> bool:
        output = subprocess.check_output(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}"], shell=True, encoding="utf-8"
        )
        processes = [line.split()[0] for line in output.splitlines()[3:]]
        return len(processes) > 0

    def dump_manifest_config(self, manifest_config: ManifestConfig, path: Optional[os.PathLike] = None) -> Path:
        path = (Path(path or self.watched_folder) / f"manifest_{manifest_config.name}.yaml").resolve()
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(manifest_config.model_dump(), f, default_flow_style=False)
        return path
