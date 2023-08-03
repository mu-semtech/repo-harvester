import unittest

from src.tests.test_config_conf import TestConfig


if __name__ == "__main__":
    suites = []
    for suite in [
        TestConfig
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()