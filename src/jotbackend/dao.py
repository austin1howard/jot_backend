from jotbackend.domain import Jot
from jotbackend.motorconn import client, database, engine, touch


async def create_jot(jot: Jot):
    await engine().save(jot)
