import requests
from flask import jsonify

from rpc_proxy.config import config_get
from rpc_proxy.proxy.request import get_request, RpcRequest


def http_tunnel(url: str, request: RpcRequest) -> dict:
    resp = requests.post(url, request.data)

    return resp.json()


def tunnel():
    request = get_request()

    if request is None:
        return {"error": "Not a valid query"}, 406

    path = "{}.{}".format(request.api, request.method)

    try:
        endpoint_target = config_get("endpoints", path)
    except KeyError:
        return {"error": "Not a valid endpoint: {}".format(path)}, 406

    try:
        instance = config_get("instances", endpoint_target)
    except KeyError:
        return {"error": "Not a valid instance: {}".format(endpoint_target)}, 406

    resp = http_tunnel(instance, request)

    return jsonify(resp)
