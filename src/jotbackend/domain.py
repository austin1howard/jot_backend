"""
Domain objects
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, TypeVar

from odmantic import EmbeddedModel
from odmantic import Field as ODField
from odmantic import Model
from pydantic import BaseModel, BaseSettings
from pydantic import Field as PydField

HandlerData = TypeVar("HandlerData", bound=EmbeddedModel)


class CreateJot(BaseModel):
    """
    A Jot for creation, as submitted through the API.
    """

    plain_text: str
    latitude: Optional[float] = PydField(..., ge=-90, le=90)
    longitude: Optional[float] = PydField(..., ge=-180, le=180)


class Jot(Model):
    """
    A "Jot" is an individual quick note from the app. It includes the text and other collected metadata.

    Eventually it's handed off to some other integration, or marked complete if trivial.
    """

    plain_text: str
    created_at: datetime
    # Can't do Optional embedded models until https://github.com/art049/odmantic/pull/273 is merged.
    latitude: Optional[float] = ODField(..., ge=-90, le=90)
    longitude: Optional[float] = ODField(..., ge=-180, le=180)
    handled: bool = False
    handler_data: Optional[HandlerData] = None


class RuntimeSettings(BaseSettings):
    class Config:
        # Used only in local development. Deployments will automatically use system environment variables.
        env_file = ".env." + os.environ.get("JOT_ENV", "local")
        env_prefix = "JOT_"
        case_sensitive = False

    mongodb_endpoint: str
    mongodb_user: Optional[str]
    mongodb_pass: Optional[str]
    mongodb_cert: Optional[Path]
    mongodb_db_name: str = "jot_mongo"

    jwt_secret: str
    jwt_issuer: str = "jot"


runtime_settings = RuntimeSettings()
