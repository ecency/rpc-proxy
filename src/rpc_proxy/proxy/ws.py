import re
from typing import Dict, Optional

from websocket import create_connection, WebSocket, WebSocketException

from rpc_proxy.config import config_get
from rpc_proxy.regex import *

WS: Optional[Dict[str, WebSocket]] = None


def init_sockets():
    global WS

    WS = {}
    instances: Dict[str, str] = config_get("instances")
    for address in instances.values():
        if re.match(WS_RE, address):
            sock = create_connection(address, timeout=0.5)
            try:
                sock.send("test")
                sock.recv()
            except WebSocketException:
                raise Exception("Web socket connection could not be created: {}".format(address))

            WS[address] = sock


def get_socket(address: str) -> Optional[WebSocket]:
    if WS is None:
        init_sockets()

    if address in WS:
        return WS[address]

    return None
