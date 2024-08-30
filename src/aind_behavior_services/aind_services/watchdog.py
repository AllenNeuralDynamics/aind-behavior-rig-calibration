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
from pydantic import BaseModel

DEFAULT_EXE = "watchdog.exe"
DEFAULT_EXE_PATH = Path(os.getenv("PROGRAMDATA", ".")) / "aind-watchdog-service" / DEFAULT_EXE
DEFAULT_WATCHED_DIRECTORY = DEFAULT_EXE_PATH.parent / "manifests"
DEFAULT_COMPLETED_DIRECTORY = DEFAULT_EXE_PATH.parent / "completed"


class Watchdog:
    """A class to interact with the AIND Watchdog service"""

    def __init__(
        self,
        schedule_time: Optional[datetime.time] = datetime.time(hour=20),
        executable: os.PathLike = DEFAULT_EXE_PATH,
        watched_dir: os.PathLike = DEFAULT_WATCHED_DIRECTORY,
        completed_dir: os.PathLike = DEFAULT_COMPLETED_DIRECTORY,
        project_name: Optional[str] = None,
        platform: Platform = getattr(Platform, "BEHAVIOR"),
        capsule_id: Optional[str] = None,
        script: Optional[Dict[str, List[str]]] = None,
        s3_bucket: BucketType = BucketType.PRIVATE,
        mount: Optional[str] = None,
        force_cloud_sync: bool = True,
        transfer_endpoint: str = "http://aind-data-transfer-service/api/v1/submit_jobs",
        validate_project_name: bool = True,
    ) -> None:
        self.project_name = project_name
        self.schedule_time = schedule_time
        self.platform = platform
        self.capsule_id = capsule_id
        self.script = script
        self.s3_bucket = s3_bucket
        self.mount = mount
        self.force_cloud_sync = force_cloud_sync
        self.transfer_endpoint = transfer_endpoint
        self._validate_project_name = validate_project_name

        self.executable = Path(executable)
        self.watched_dir = Path(watched_dir)
        self.completed_dir = Path(completed_dir)

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

    def create_manifest_config(
        self,
        source: os.PathLike,
        destination: os.PathLike,
        ads_session: Session,
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
        validate_project_name = kwargs.pop("validate_project_name", self._validate_project_name)
        processor_full_name = (
            kwargs.pop("processor_full_name", None)
            or ",".join(ads_session.experimenter_full_name)
            or os.environ.get("USERNAME", "unknown")
        )

        destination = Path(destination).resolve()
        source = Path(source).resolve()

        if session_name is None:
            session_name = (ads_session.stimulus_epochs[0]).stimulus_name

        if validate_project_name:
            project_names = Watchdog._get_project_names()
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
            jData = json.loads(response.content)
        else:
            response.raise_for_status()
        return jData["data"]

    @staticmethod
    def is_running(process_name: str = DEFAULT_EXE) -> bool:
        output = subprocess.check_output(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}"], shell=True, encoding="utf-8"
        )
        processes = [line.split()[0] for line in output.splitlines()[3:]]
        return len(processes) > 0

    def force_restart(self, kill_if_running: bool = True) -> subprocess.Popen[bytes]:
        if kill_if_running is True:
            while self.is_running():
                subprocess.run(["taskkill", "/IM", DEFAULT_EXE, "/F"], shell=True, check=True)

        cmd_builder = "{exe} -f {watched_dir} -m {completed_dir}".format(
            exe=self.executable, watched_dir=self.watched_dir, completed_dir=self.completed_dir
        )

        return subprocess.Popen(cmd_builder, start_new_session=True, shell=True)

    def dump_manifest_config(
        self, manifest_config: ManifestConfig, path: Optional[os.PathLike] = None, make_dir: bool = True
    ) -> Path:
        path = Path(path if path else self.watched_dir / f"manifest_{manifest_config.name}.yaml").resolve()
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

        with open(path, "w", encoding="utf-8") as f:
            f.write(self._yaml_dump(manifest_config))
        return path

    @staticmethod
    def _yaml_dump(model: BaseModel) -> str:
        native_json = json.loads(model.model_dump_json())
        return yaml.dump(native_json, default_flow_style=False)
