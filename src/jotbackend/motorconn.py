import asyncio

from clearcut import get_logger_tracer
from jitproxy import StandardLazyProxy
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from odmantic.engine import AIOEngine, ModelType

from jotbackend.domain import runtime_settings

logger, tracer = get_logger_tracer(__name__)


def touch(model_inst: ModelType) -> None:
    """Similar to unix `touch`, marks all fields in instance as 'updated', forcing an overwrite on next `save`."""
    object.__setattr__(model_inst, "__fields_modified__", set(model_inst.__odm_fields__.keys()))


class FixedAsyncIOMotorClient(AsyncIOMotorClient):
    def __init__(self, *args, **kwargs):

        # Workaround for motor + anyio fighting: see https://github.com/encode/starlette/issues/1315#issuecomment-994941490
        super().__init__(*args, **kwargs)
        self.get_io_loop = asyncio.get_event_loop


# Get MongoDB connection info
if runtime_settings.mongodb_pass is not None and runtime_settings.mongodb_pass != "":
    _client: StandardLazyProxy[FixedAsyncIOMotorClient] = StandardLazyProxy(FixedAsyncIOMotorClient)(
        runtime_settings.mongodb_endpoint, username=runtime_settings.mongodb_user, password=runtime_settings.mongodb_pass
    )
elif runtime_settings.mongodb_cert is not None and runtime_settings.mongodb_cert != "":
    _client: StandardLazyProxy[FixedAsyncIOMotorClient] = StandardLazyProxy(FixedAsyncIOMotorClient)(
        runtime_settings.mongodb_endpoint,
        username=runtime_settings.mongodb_user,
        tlsCertificateKeyFile=str(runtime_settings.mongodb_cert.absolute()),
        tlsCAFile=str(runtime_settings.mongodb_cert.absolute()),
        tlsAllowInvalidCertificates=True,
    )
else:
    _client: StandardLazyProxy[FixedAsyncIOMotorClient] = StandardLazyProxy(FixedAsyncIOMotorClient)(
        runtime_settings.mongodb_endpoint, username=runtime_settings.mongodb_user
    )


def client():
    return _client.__


_engine: StandardLazyProxy[AIOEngine] = StandardLazyProxy(AIOEngine)(client=_client, database=runtime_settings.mongodb_db_name)


def engine():
    return _engine.__


database: StandardLazyProxy[AsyncIOMotorDatabase] = StandardLazyProxy(AsyncIOMotorDatabase)(_client, runtime_settings.mongodb_db_name)
