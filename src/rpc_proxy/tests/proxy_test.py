import unittest

from rpc_proxy.request import parse_request


class ProxyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = 1000

    def test_parse_request_01(self):
        # should read api and method from "method"
        inpt = '{"jsonrpc":"2.0", "method":"bridge.get_ranked_posts", "params":{"sort":"trending","tag":"","observer":"alice"}, "id":1}'
        expected = "rpc_ver: 2.0, api: bridge, method: get_ranked_posts, params: {'sort': 'trending', 'tag': '', 'observer': 'alice'}, id:1"
        self.assertEqual(str(parse_request(inpt)), expected)

    def test_parse_request_02(self):
        # should read api and method from "params"
        inpt = '{"jsonrpc":"2.0", "method":"call", "params": ["condenser_api", "get_follow_count", ["alice"]], "id":1}'
        expected = "rpc_ver: 2.0, api: condenser_api, method: get_follow_count, params: ['alice'], id:1"
        self.assertEqual(str(parse_request(inpt)), expected)

    def test_parse_request_03(self):
        # should create empty "params" field if not provided
        inpt = '{"jsonrpc":"2.0", "method":"database_api.get_dynamic_global_properties", "id":1}'
        expected = "rpc_ver: 2.0, api: database_api, method: get_dynamic_global_properties, params: [], id:1"
        self.assertEqual(str(parse_request(inpt)), expected)
