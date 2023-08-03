import unittest

from src.tests.test_config_conf import TestConfig
from src.tests.test_config_override import TestConfigOverride


if __name__ == "__main__":
    suites = []
    for suite in [
        TestConfig,
        TestConfigOverride
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()