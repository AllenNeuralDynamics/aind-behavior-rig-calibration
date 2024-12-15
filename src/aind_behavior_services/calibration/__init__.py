from __future__ import annotations

import datetime
import logging
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Calibration(BaseModel):
    """Base class for all Calibration models. Stores calibration (meta)data."""

    device_name: str = Field(..., title="Device name", description="Name of the device being calibrated")
    input: Optional[BaseModel] = Field(default=None, title="Input data")
    output: Optional[BaseModel] = Field(default=None, title="Output data")
    date: Optional[datetime.datetime] = Field(default=None, title="Date")
    description: Optional[str] = Field(default=None, title="Brief description of what is being calibrated")
    notes: Optional[str] = Field(default=None, title="Notes")
