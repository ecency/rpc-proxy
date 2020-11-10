import re
from typing import Dict, Optional

from websockets import connect, WebSocketClientProtocol

from rpc_proxy.config import config_get, config_get_timeout
from rpc_proxy.logger import create_logger
from rpc_proxy.regex import *

logger = create_logger("ws")

_ws: Optional[Dict[str, WebSocketClientProtocol]] = None


async def init_sockets():
    global _ws

    _ws = {}
    targets: Dict[str, str] = config_get("targets")
    for k in targets.keys():
        address = targets[k]
        if re.match(WS_RE, address):
            try:
                sock = await connect(address, timeout=config_get_timeout(k))
            except BaseException as ex:
                msg = "Web socket connection could not be created: {} - {}".format(address, str(ex))
                logger.error(msg)
                raise Exception(msg)

            _ws[address] = sock


async def get_socket(address: str) -> Optional[WebSocketClientProtocol]:
    if _ws is None:
        await init_sockets()

    if address in _ws:
        return _ws[address]

    return None
