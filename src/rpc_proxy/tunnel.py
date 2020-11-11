import json
import re
from typing import Dict, Optional

import requests
from sanic import response

from rpc_proxy.cache import cache_get, cache_set
from rpc_proxy.config import config_get, config_get_timeout, NoSuchConfigException
from rpc_proxy.helper import route_match
from rpc_proxy.logger import create_logger
from rpc_proxy.regex import *
from rpc_proxy.request import parse_request, translate_to_app_base
from rpc_proxy.util import assert_env_vars
from rpc_proxy.ws import get_socket

logger = create_logger("tunnel")

try:
    assert_env_vars("LOG_ERRORS")
    LOG_ERRORS = True
except AssertionError:
    LOG_ERRORS = False


async def http_tunnel(url: str, payload: str, timeout: int) -> Dict:
    resp = requests.post(url, payload, timeout=timeout)

    return resp.json()


async def ws_tunnel(url: str, payload: str, timeout: int) -> Dict:
    sock = await get_socket(url)

    await sock.send(payload)

    resp = await sock.recv()

    return json.loads(resp)


async def sock_tunnel(url: str, payload: str, timeout: int) -> Dict:
    raise NotImplementedError


def success_response(data: Dict, from_cache: bool, source: str, path: str, route: str):
    return response.json(
        data,
        headers={
            "rpc-proxy-from-cache": "1" if from_cache else "0",
            "rpc-proxy-data-source": source,
            "rpc-proxy-path": path,
            "rpc-proxy-route": route,
            "Access-Control-Expose-Headers": "*"
        },
        status=200
    )


def error_response(data: Dict, status: int):
    return response.json(
        data,
        headers={
            "Access-Control-Expose-Headers": "*"
        },
        status=status
    )


async def tunnel(data: Optional[Dict]):
    request = parse_request(data)

    if request is None:
        return error_response({"error": "Not a valid json request"}, 406)

    path = "{}.{}".format(request.api, request.method)

    route = route_match(config_get("routes"), path)

    if route is None:
        return error_response({"error": "No route has matched: '{}'".format(path)}, 406)

    route_config = config_get("routes", route)

    if "translate_to_app_base" in route_config:
        request = translate_to_app_base(request)

    target_name = route_config["target"]

    payload = json.dumps(request.data)

    try:
        target: str = config_get("targets", target_name)
    except NoSuchConfigException:
        return error_response({"error": "Not a valid target: {}".format(target_name)}, 406)

    cache_timeout: int = config_get("default-cache")
    if "cache" in route_config:
        cache_timeout = route_config["cache"]

    cache_key = "{}_{}".format(path, hash(str(request.params)))

    if cache_timeout > 0:
        resp = await cache_get(cache_key)
        if resp is not None:
            return success_response(resp, True, target_name, path, route)

    timeout = config_get_timeout(target_name)

    if re.match(HTTP_RE, target):
        fn = http_tunnel
    elif re.match(WS_RE, target):
        fn = ws_tunnel
    elif re.match(SOCK_RE, target):
        fn = sock_tunnel
    else:
        return error_response({"error": "Not a valid scheme: {}".format(target)}, 406)

    try:
        resp = await fn(*(target, payload, timeout))
    except BaseException as ex:
        return error_response({"error": str(ex)}, 500)

    if LOG_ERRORS and "error" in resp:
        logger.error("Query failed: {} - {}".format(request.data, json.dumps(resp)))

    if "error" not in resp and cache_timeout > 0:
        await cache_set(cache_key, resp, cache_timeout)

    return success_response(resp, False, target_name, path, route)
