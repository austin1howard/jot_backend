"""
Creates a task in Reclaim.
"""
from datetime import datetime
from enum import Enum

from clearcut import get_logger
from odmantic import EmbeddedModel

from jotbackend.domain import Jot
from jotbackend.handlers.base import BaseHandler

logger = get_logger(__name__)


class ReclaimTaskType(Enum):
    WORKING = "working"
    PERSONAL = "personal"


class ReclaimData(EmbeddedModel):
    """
    Data required to create a task in Reclaim.
    """

    task_name: str
    task_notes: str
    task_type: ReclaimTaskType
    task_duration: float
    task_min_block_duration: float
    task_max_block_duration: float
    task_block_start: datetime
    task_block_end: datetime


class ReclaimHandler(BaseHandler):
    """
    Creates a task in Reclaim.
    """

    @property
    def name(self) -> str:
        return "reclaim"

    def backend_handle(self, jot: Jot) -> Jot:
        """
        Handle a Jot with the provided kwargs. This is executed on the backend.
        """
        return jot

    def frontend_handle_data(self, jot: Jot) -> dict:
        """
        This is data used by the frontend if that's what handles the Jot.
        """
        return {}
