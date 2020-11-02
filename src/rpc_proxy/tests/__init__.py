import unittest

from .proxy_test import ProxyTestCase


def make_suite():
    test_1 = unittest.TestLoader().loadTestsFromTestCase(ProxyTestCase)

    suite = unittest.TestSuite(
        [test_1, ]
    )

    return suite


def do_tests():
    runner = unittest.TextTestRunner()
    test_suite = make_suite()
    runner.run(test_suite)
