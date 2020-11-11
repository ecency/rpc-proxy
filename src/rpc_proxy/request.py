from typing import Optional, Dict


class RpcRequest:
    def __init__(self, data: Dict, rpc_ver: str, api: str, method: str, params: dict, _id: str):
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


def parse_request(js_data: Optional[Dict]) -> Optional[RpcRequest]:
    if js_data is None:
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

    return RpcRequest(js_data, rpc_ver, api, method, params, _id)


def translate_to_app_base(req: RpcRequest):
    params = []

    if isinstance(req.params, dict):
        for item in req.params.items():
            params.append(item[1])

    if isinstance(req.params, list):
        params = req.params

    js_data = {
        "id": req.id,
        "jsonrpc": req.rpc_ver,
        "method": "call",
        "params": ["condenser_api", req.method, params]
    }

    return parse_request(js_data)
