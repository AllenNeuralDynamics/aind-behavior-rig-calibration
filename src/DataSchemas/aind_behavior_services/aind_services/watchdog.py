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
from pathlib import Path
from typing import Dict, List, Literal, Optional

import requests
from aind_data_schema.core.session import Session
from aind_watchdog_service.models.manifest_config import ManifestConfig, Platform
from aind_watchdog_service.models.watch_config import WatchConfig


def create_watchdog_config(
    watched_directory: os.PathLike, manifest_complete_directory: os.PathLike, webhook_url: Optional[str] = None
) -> WatchConfig:
    """Create a WatchConfig object"""
    return WatchConfig(
        watched_directory=str(watched_directory),
        manifest_complete=str(manifest_complete_directory),
        webhook_url=webhook_url,
    )


def create_manifest_config(
    session: Session,
    source: os.PathLike,
    destination: os.PathLike,
    project_name: str,
    session_name: Optional[str] = None,
    processor_full_name: Optional[str] = None,
    schedule_time: Optional[
        datetime.datetime
    ] = None,  # TODO https://github.com/AllenNeuralDynamics/aind-watchdog-service/pull/37
    platform: str = Platform.BEHAVIOR.abbreviation,
    capsule_id: Optional[str] = None,
    script: Optional[Dict[str, List[str]]] = None,
    s3_bucket: Literal["s3", "public", "private", "scratch"] = "private",
    mount: Optional[str] = None,
    /,
    validate_project_name: bool = True,
) -> ManifestConfig:
    """Create a ManifestConfig object"""
    processor_full_name = processor_full_name or os.environ.get("USERNAME")

    destination = Path(destination).resolve()
    source = Path(source).resolve()

    if session_name is None:
        session_name = (session.stimulus_epochs[0]).stimulus_name

    if validate_project_name:
        project_names = _get_project_names()
        if project_name not in project_names:
            raise ValueError(f"Project name {project_name} not found in {project_names}")

    return ManifestConfig(
        name=session_name,
        modalities={
            str(modality.abbreviation): [source / str(modality.abbreviation)]
            for modality in session.data_streams[0].stream_modalities
        },
        subject_id=session.subject_id,
        acquisition_datetime=session.session_start_time,
        schemas=[source / "session.json", source / "other"],
        destination=destination,
        mount=mount,
        processor_full_name=processor_full_name,
        project_name=project_name,
        schedule_time=schedule_time,
        platform=platform,
        capsule_id=capsule_id,
        s3_bucket=s3_bucket,
        script=script,
    )


def _get_project_names(end_point: str = "http://aind-metadata-service/project_names", timeout: int = 5) -> list[str]:
    response = requests.get(end_point, timeout=timeout)
    if response.ok:
        jData = json.loads(response.content)

    else:
        response.raise_for_status()
    return jData["data"]
