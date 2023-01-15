"""
Base class for all Jot handlers.
"""

import abc
from typing import Generic, Optional, Type

from clearcut import get_logger

from jotbackend.domain import HandlerData, Jot

logger = get_logger(__name__)


class BaseHandler(abc.ABC, Generic[HandlerData]):
    """
    Base class for all Jot handlers. A handler instance is a particular solution to handle a Jot. This might be suggested
    by a model, or provided by the user.
    """

    handlers: dict[str, Type["BaseHandler"]] = {}

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.name in cls.handlers:
            raise ValueError(f"Duplicate handler name {cls.name}")

        cls.handlers[cls.name()] = cls

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        """
        The name of the handler.
        """
        pass

    def __init__(self) -> None:
        self._ready_to_handle = False
        self._handler_data = {}

    @property
    def handler_data(self):
        return self._handler_data

    @handler_data.setter
    def handler_data(self, data: Optional[HandlerData]):
        self._handler_data = data
        self._ready_to_handle = True

    @property
    def ready_to_handle(self):
        return self._ready_to_handle

    @abc.abstractmethod
    def backend_handle(self, jot: Jot) -> Jot:
        """
        Handle a Jot with the provided kwargs. This is executed on the backend.
        """
        pass

    @abc.abstractmethod
    def frontend_handle_data(self, jot: Jot) -> dict:
        """
        This is data used by the frontend if that's what handles the Jot.
        """
        pass
