from os import PathLike
from typing import Optional

try:
    import aind_watchdog_service  # noqa: F401
except ImportError as e:
    e.add_note(
        "The 'aind-watchdog-service' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-extra-services]`"
    )
    raise

from aind_watchdog_service.models.manifest_config import ManifestConfig
from aind_watchdog_service.models.watch_config import WatchConfig


def create_watchdog_config(
    watched_directory: PathLike, manifest_complete_directory: PathLike, webhook_url: Optional[str] = None
) -> WatchConfig:
    """Create a WatchConfig object"""
    return WatchConfig(
        watched_directory=str(watched_directory),
        manifest_complete=str(manifest_complete_directory),
        webhook_url=webhook_url,
    )
