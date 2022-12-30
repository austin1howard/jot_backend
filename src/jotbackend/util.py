import asyncio

import uvicorn


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
