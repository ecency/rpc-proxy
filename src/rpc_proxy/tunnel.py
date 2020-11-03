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

    instance_name = config_get("routes", route)

    try:
        instance: str = config_get("instances", instance_name)
    except NoSuchConfigException:
        return {"error": "Not a valid instance: {}".format(instance_name)}, 406

    timeout = config_get_timeout(instance_name)

    if re.match(HTTP_RE, instance):
        fn = http_tunnel
    elif re.match(WS_RE, instance):
        fn = ws_tunnel
    elif re.match(SOCK_RE, instance):
        fn = sock_tunnel
    else:
        return {"error": "Not a valid scheme: {}".format(instance)}, 406

    try:
        resp = fn(*(instance, request, timeout))
    except BaseException as ex:
        return {"error": str(ex)}

    return jsonify(resp)
