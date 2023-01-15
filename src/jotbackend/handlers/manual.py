"""
Manual handler. Does nothing but mark the Jot as handled.
"""
from odmantic import EmbeddedModel

from jotbackend.domain import Jot
from jotbackend.handlers.base import BaseHandler


class ManualData(EmbeddedModel):
    pass


class ManualHandler(BaseHandler[ManualData]):
    """
    NoOp.
    """

    @property
    def name(self) -> str:
        return "manual"

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
