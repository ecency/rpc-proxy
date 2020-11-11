import unittest
import json

from rpc_proxy.request import parse_request, translate_to_app_base


class ProxyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = 1000

    def test_parse_request_01(self):
        # should read api and method from "method"
        js = '{"jsonrpc":"2.0", "method":"bridge.get_ranked_posts", "params":{"sort":"trending","tag":"","observer":"alice"}, "id":1}'
        js_data = json.loads(js)
        expected = "rpc_ver: 2.0, api: bridge, method: get_ranked_posts, params: {'sort': 'trending', 'tag': '', 'observer': 'alice'}, id:1"
        self.assertEqual(str(parse_request(js_data)), expected)

    def test_parse_request_02(self):
        # should read api and method from "params"
        js = '{"jsonrpc":"2.0", "method":"call", "params": ["condenser_api", "get_follow_count", ["alice"]], "id":1}'
        js_data = json.loads(js)
        expected = "rpc_ver: 2.0, api: condenser_api, method: get_follow_count, params: ['alice'], id:1"
        self.assertEqual(str(parse_request(js_data)), expected)

    def test_parse_request_03(self):
        # should create empty "params" field if not provided
        js = '{"jsonrpc":"2.0", "method":"database_api.get_dynamic_global_properties", "id":1}'
        js_data = json.loads(js)
        expected = "rpc_ver: 2.0, api: database_api, method: get_dynamic_global_properties, params: [], id:1"
        self.assertEqual(str(parse_request(js_data)), expected)

    def test_translate_app_base(self):
        """
        ## With empty dict params
        """
        js = '{"id": 85, "jsonrpc": "2.0", "method": "database_api.get_version", "params": {}}'
        js_data = json.loads(js)
        req = parse_request(js_data)
        expected = "{'id': 85, 'jsonrpc': '2.0', 'method': 'call', 'params': ['condenser_api', 'get_version', []]}"
        self.assertEqual(str(translate_to_app_base(req).data), expected)

        """
        ## No params provided
        """
        js = '{"id": 85, "jsonrpc": "2.0", "method": "database_api.get_version"}'
        js_data = json.loads(js)
        req = parse_request(js_data)
        expected = "{'id': 85, 'jsonrpc': '2.0', 'method': 'call', 'params': ['condenser_api', 'get_version', []]}"
        self.assertEqual(str(translate_to_app_base(req).data), expected)

        """
        ## Params provided with list
        """
        js = '{"id": 85, "jsonrpc": "2.0", "method": "condenser_api.get_following", "params":["hiveio",null,"blog",10]}'
        js_data = json.loads(js)
        req = parse_request(js_data)
        expected = "{'id': 85, 'jsonrpc': '2.0', 'method': 'call', 'params': ['condenser_api', 'get_following', ['hiveio', None, 'blog', 10]]}"
        self.assertEqual(str(translate_to_app_base(req).data), expected)

        """
        ## Params provided with dict
        """
        js = '{"id": 85, "jsonrpc": "2.0", "method": "condenser_api.get_following", "params": {"foo":"bar"}}'
        js_data = json.loads(js)
        req = parse_request(js_data)
        expected = "{'id': 85, 'jsonrpc': '2.0', 'method': 'call', 'params': ['condenser_api', 'get_following', ['bar']]}"
        self.assertEqual(str(translate_to_app_base(req).data), expected)
