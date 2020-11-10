from typing import Optional

from sanic import Sanic
from sanic.request import Request

from rpc_proxy.logger import create_logger
from rpc_proxy.tunnel import tunnel
from rpc_proxy.util import assert_env_vars

app = Optional[Sanic]

logger = create_logger('proxy')


def __app_setup():
    global app

    app = Sanic()

    @app.route("/", methods=["POST"])
    async def index(request: Request):
        return await tunnel(request.json)


def run_server():
    args = {}

    logger.info("Starting..")
    logger.info("#" * 20)

    for item in {
        "HOST": "127.0.0.1",
        "PORT": 8080,
        "WORKERS": 4,
        "DEBUG": False
    }.items():
        [k, v] = item

        try:
            val = type(v)(assert_env_vars(k))
        except (AssertionError, ValueError):
            val = v

        args[k.lower()] = val

        logger.info("{}: {}".format(k, val))

    logger.info("#" * 20)

    app.run(**args)


__app_setup()


def main():
    run_server()
