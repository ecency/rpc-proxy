import re
from typing import Dict, Optional

from websocket import create_connection, WebSocket, WebSocketException

from rpc_proxy.config import config_get
from rpc_proxy.regex import *

_ws: Optional[Dict[str, WebSocket]] = None


def init_sockets():
    global _ws

    timeouts = config_get("timeouts")

    _ws = {}
    instances: Dict[str, str] = config_get("instances")
    for k in instances.keys():
        address = instances[k]
        if re.match(WS_RE, address):

            if isinstance(timeouts, int):
                timeout = timeouts
            else:
                timeout = config_get("timeouts", k)

            sock = create_connection(address, timeout=timeout)

            try:
                sock.send("test")
                sock.recv()
            except WebSocketException:
                raise Exception("Web socket connection could not be created: {}".format(address))

            _ws[address] = sock


def get_socket(address: str) -> Optional[WebSocket]:
    if _ws is None:
        init_sockets()

    if address in _ws:
        return _ws[address]

    return None
