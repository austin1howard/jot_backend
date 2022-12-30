import asyncio

import uvicorn
from clearcut import get_logger
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWSError, JWTError, jwt

from jotbackend.domain import runtime_settings

logger = get_logger(__name__)


def narvhal(app, port):
    """
    Creates and starts the uvicorn server, but using an existing loop instead of forcing a new one and breaking
    everything with "...attached to a different loop".
    """
    # Override logging format
    uvicorn_logging_format = '%(asctime)s [%(levelname)s] (HTTP | %(client_addr)s) | "%(request_line)s" %(status_code)s'
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = uvicorn_logging_format

    # `uvicorn.run` calls `Server.run` which calls `asyncio.run`, which makes a new loop always (and thus causes problems with anything
    # that's been imported so far. So we use the lower level api.

    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_config=log_config, loop="none")

    server = uvicorn.Server(config=config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())


def credentials_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail: str = "Could not validate credentials"):
    return HTTPException(status_code=status_code, detail=detail, headers={"WWW-Authenticate": "Bearer"})


def get_subject_from_token(token: str):
    """Checks JWT token and returns subject (email address) if valid."""
    try:
        # Check that token was provided at all
        if token is None or token == "":
            raise credentials_exception(detail="Credentials not provided")

        # decode and validate token
        try:
            payload = jwt.decode(token, runtime_settings.jwt_secret, issuer=runtime_settings.jwt_issuer)
        except ExpiredSignatureError:
            raise credentials_exception(detail="Token has expired")

        # subject is email address
        email_address: str = payload.get("sub")
        if email_address is None:
            raise credentials_exception(detail="Email not present in token")

        return email_address
    except (JWTError, JWSError) as e:
        logger.error("JWTError being suppressed, credentials exception will be raised instead", exc_info=e)
        raise credentials_exception(detail="Token is not valid")
