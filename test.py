import unittest

from src.tests.test_config_conf import TestConfig
from src.tests.test_config_override import TestConfigOverride
from src.tests.test_utils_categories import TestUtilsCategories
from src.tests.imagesource.t_imgsrc_class import TestImagesourceClass

if __name__ == "__main__":
    suites = []
    for suite in [
        TestConfig,
        TestConfigOverride,
        TestUtilsCategories,
        TestImagesourceClass
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()