import requests
from flask import jsonify
import re

from rpc_proxy.config import config_get
from rpc_proxy.proxy.request import get_request, RpcRequest
from typing import Optional, Dict


class Response:
    def __init__(self, status: bool, json: Optional[Dict] = None):
        self.status = status
        self.json = json


def http_tunnel(url: str, request: RpcRequest) -> Response:
    resp = requests.post(url, request.data)

    return Response(True, resp.json())


def ws_tunnel(url: str, request: RpcRequest) -> Response:
    raise NotImplementedError


def sock_tunnel(url: str, request: RpcRequest) -> Response:
    raise NotImplementedError


def tunnel():
    request = get_request()

    if request is None:
        return {"error": "Not a valid json request"}, 406

    path = "{}.{}".format(request.api, request.method)

    try:
        endpoint_target = config_get("endpoints", path)
    except KeyError:
        return {"error": "Not a valid endpoint: {}".format(path)}, 406

    try:
        instance: str = config_get("instances", endpoint_target)
    except KeyError:
        return {"error": "Not a valid instance: {}".format(endpoint_target)}, 406

    if re.match("^(http|https)://", instance):
        resp = http_tunnel(instance, request)
    elif re.match("^(ws|wss)://", instance):
        resp = ws_tunnel(instance, request)
    elif instance.startswith("sock://"):
        resp = sock_tunnel(instance, request)
    else:
        return {"error": "Not a valid scheme: {}".format(instance)}, 406

    return jsonify(resp.json)
