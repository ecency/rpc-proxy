import json
import re
from typing import Dict

import requests
from flask import Response

from rpc_proxy.cache import cache
from rpc_proxy.config import config_get, config_get_timeout, NoSuchConfigException
from rpc_proxy.helper import route_match
from rpc_proxy.regex import *
from rpc_proxy.request import get_request, RpcRequest
from rpc_proxy.ws import get_socket


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


def make_response(data: str, from_cache: bool, source: str):
    return Response(
        response=data,
        mimetype='application/json',
        headers={
            "rpc-proxy-from-cache": "1" if from_cache else "0",
            "rpc-proxy-data-source": source
        }
    )


def tunnel():
    request = get_request()

    if request is None:
        return {"error": "Not a valid json request"}, 406

    path = "{}.{}".format(request.api, request.method)

    route = route_match(config_get("routes"), path)

    if route is None:
        return {"error": "No route has matched: '{}'".format(path)}, 406

    route_config = config_get("routes", route)

    target_name = route_config["target"]

    try:
        target: str = config_get("targets", target_name)
    except NoSuchConfigException:
        return {"error": "Not a valid target: {}".format(target_name)}, 406

    cache_timeout: int = config_get("default-cache")
    if "cache" in route_config:
        cache_timeout = route_config["cache"]

    cache_key = "{}_{}".format(path, hash(str(request.params)))

    if cache_timeout > 0:
        resp = cache.get(cache_key)
        if resp is not None:
            return make_response(json.dumps(resp), True, target_name)

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

    if "error" not in resp and cache_timeout > 0:
        cache.set(cache_key, resp, timeout=cache_timeout)

    return make_response(json.dumps(resp), False, target_name)
