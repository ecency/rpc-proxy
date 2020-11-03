import unittest

from .proxy_test import ProxyTestCase
from .helper_test import HelperTestCase


def make_suite():
    test_1 = unittest.TestLoader().loadTestsFromTestCase(ProxyTestCase)
    test_2 = unittest.TestLoader().loadTestsFromTestCase(HelperTestCase)

    suite = unittest.TestSuite(
        [test_1, test_2, ]
    )

    return suite


def do_tests():
    runner = unittest.TextTestRunner()
    test_suite = make_suite()
    runner.run(test_suite)
