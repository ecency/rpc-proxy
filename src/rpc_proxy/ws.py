import re
from typing import Dict, Optional

from websocket import create_connection, WebSocket

from rpc_proxy.config import config_get, config_get_timeout
from rpc_proxy.logger import create_logger
from rpc_proxy.regex import *

logger = create_logger("ws")

_ws: Optional[Dict[str, WebSocket]] = None


def init_sockets():
    global _ws

    _ws = {}
    instances: Dict[str, str] = config_get("instances")
    for k in instances.keys():
        address = instances[k]
        if re.match(WS_RE, address):
            try:
                sock = create_connection(address, timeout=config_get_timeout(k))
            except BaseException as ex:
                msg = "Web socket connection could not be created: {} - {}".format(address, str(ex))
                logger.error(msg)
                raise Exception(msg)

            _ws[address] = sock


def get_socket(address: str) -> Optional[WebSocket]:
    if _ws is None:
        init_sockets()

    if address in _ws:
        return _ws[address]

    return None
