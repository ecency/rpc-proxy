import json
from typing import Optional

from flask import request


class RpcRequest:
    def __init__(self, data: str, rpc_ver: str, api: str, method: str, params: dict, _id: str):
        self.data = data
        self.rpc_ver = rpc_ver
        self.api = api
        self.method = method
        self.params = params
        self.id = _id

    def __repr__(self):
        return "rpc_ver: {}, api: {}, method: {}, params: {}, id:{}".format(
            self.rpc_ver, self.api, self.method, self.params, self.id
        )


def get_request() -> Optional[RpcRequest]:
    data = request.get_data().decode()

    return parse_request(data)


def parse_request(data: str) -> Optional[RpcRequest]:
    try:
        js_data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return None

    if "jsonrpc" in js_data and "method" in js_data and "id" in js_data:
        rpc_ver = js_data["jsonrpc"]
        raw_method = js_data["method"]
        params = js_data["params"] if "params" in js_data else []
        _id = js_data["id"]
    else:
        return None

    if raw_method == "call":
        [api, method, params] = params
    else:
        [api, method] = raw_method.split(".")

    return RpcRequest(data, rpc_ver, api, method, params, _id)
