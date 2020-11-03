import unittest

from rpc_proxy.helper import route_match


class HelperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_route_match_01(self):
        routes = ["^bridge.get_post$", "^database_api.(.*)", "^condenser_api.(.*)", "^network_broadcast_api(.*)"]

        self.assertEqual(route_match(routes, "condenser_api.get_dynamic_global_properties"), "^condenser_api.(.*)")

        self.assertEqual(route_match(routes, "database_api.get_blog"), "^database_api.(.*)")

        self.assertEqual(route_match(routes, "bridge.get_post"), "^bridge.get_post$")

        self.assertEqual(route_match(routes, "unknown_api.get_data"), None)

        self.assertEqual(route_match(routes, "network_broadcast_api.broadcast_block"), "^network_broadcast_api(.*)")
