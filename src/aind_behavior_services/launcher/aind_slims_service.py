from __future__ import annotations

try:
    import aind_slims_api
except ImportError as e:
    e.add_note(
        "The 'aind-slims_api' package is required to use this module. \
            Install the optional dependencies defined in `project.toml' \
                by running `pip install .[aind-services]`"
    )
    raise

import logging
import os
from typing import Optional
import aind_slims_api.core
import aind_slims_api.models as slims_models
from aind_data_schema.core.session import Session as AdsSession

from ._service import IService

logger = logging.getLogger(__name__)

DEFAULT_USERNAME: Optional[str] = os.getenv("SLIMS_USERNAME", None)
DEFAULT_PASSWORD: Optional[str] = os.getenv("SLIMS_PASSWORD", None)
DEFAULT_URL: Optional[str] = os.getenv("SLIMS_URL", None)


class SlimsServices(IService):

    def __init__(
        self, url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        url = url or os.environ.get("SLIMS_URL", None)
        username = username or os.environ.get("SLIMS_USERNAME", None)
        password = password or os.environ.get("SLIMS_PASSWORD", None)

        if username is None or password is None or url is None:
            raise ValueError(
                "SLIMS_URL, SLIMS_USERNAME and SLIMS_PASSWORD must be provided or set as environment variables"
            )

        self._slims_client = aind_slims_api.core.SlimsClient(username=username, password=password, url=url)


    @property
    def slims_client(self) -> aind_slims_api.core.SlimsClient:
        return self._slims_client


    def fetch_model(self, *args, **kwargs) -> Optional[aind_slims_api.core.SlimsBaseModelTypeVar]:
        return self.slims_client.fetch_model(*args, **kwargs)