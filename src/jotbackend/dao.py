from typing import AsyncIterator, Optional

from odmantic import ObjectId

from jotbackend.domain import Jot
from jotbackend.handlers.base import HandlerData
from jotbackend.motorconn import engine


async def create_jot(jot: Jot):
    await engine().save(jot)


async def get_jots(include_handled: bool) -> AsyncIterator[Jot]:
    query = {}
    if not include_handled:
        query["handled"] = False

    async for jot in engine().find(Jot, query):
        yield jot


async def get_jot(id: ObjectId) -> Jot:
    return await engine().find_one(Jot, Jot.id.eq(id))


async def mark_jot_handled(id: ObjectId, handler_data: Optional[HandlerData]):
    jot = await get_jot(id)
    if jot is None:
        raise ValueError(f"Jot not found for id {id}")

    jot.handler_data = handler_data
    jot.handled = True

    await engine().save(jot)
