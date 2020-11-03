import json
import re
from typing import Optional, Dict

import requests
from flask import jsonify

from rpc_proxy.config import config_get, config_get_timeout, NoSuchConfigException
from rpc_proxy.helper import route_match
from rpc_proxy.regex import *
from rpc_proxy.request import get_request, RpcRequest
from rpc_proxy.ws import get_socket


class Response:
    def __init__(self, status: bool, data: Optional[Dict] = None):
        self.status = status
        self.data = data


def http_tunnel(url: str, request: RpcRequest, timeout: int) -> Dict:
    resp = requests.post(url, request.data, timeout=timeout)

    return resp.json()


def ws_tunnel(url: str, request: RpcRequest, timeout: int) -> Dict:
    sock = get_socket(url)

    sock.settimeout(timeout)

    sock.send(request.data)
    resp = sock.recv()

    return json.loads(resp)


def sock_tunnel(url: str, request: RpcRequest, timeout: int) -> Dict:
    raise NotImplementedError


def tunnel():
    request = get_request()

    if request is None:
        return {"error": "Not a valid json request"}, 406

    path = "{}.{}".format(request.api, request.method)

    route = route_match(config_get("routes"), path)

    if route is None:
        return {"error": "No route has matched: '{}'".format(path)}, 406

    target_name = config_get("routes", route)

    try:
        target: str = config_get("targets", target_name)
    except NoSuchConfigException:
        return {"error": "Not a valid target: {}".format(target_name)}, 406

    should_cache = route_match(config_get("no-cache"), path) is None

    timeout = config_get_timeout(target_name)

    if re.match(HTTP_RE, target):
        fn = http_tunnel
    elif re.match(WS_RE, target):
        fn = ws_tunnel
    elif re.match(SOCK_RE, target):
        fn = sock_tunnel
    else:
        return {"error": "Not a valid scheme: {}".format(target)}, 406

    try:
        resp = fn(*(target, request, timeout))
    except BaseException as ex:
        return {"error": str(ex)}

    return jsonify(resp)
