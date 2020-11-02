import requests

from rpc_proxy.config import config_get
from rpc_proxy.proxy.request import get_request


def handler():
    request = get_request()

    path = "{}.{}".format(request.api, request.method)

    endpoint_target = config_get("endpoints", path)
    instance = config_get("instances", endpoint_target)

    resp = requests.post(instance, request.data)

    return resp.json()
