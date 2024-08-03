try:
    import aind_watchdog_service  # noqa: F401
except ImportError as e:
    e.add_note(
        "The 'aind-watchdog-service' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-extra-services]`"
    )
    raise

import os
import datetime
from pathlib import Path
from typing import Optional

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

