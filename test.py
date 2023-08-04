import unittest

from src.tests.test_repo import TestRepoClass

from src.tests.config.test_conf import TestConfig
from src.tests.config.test_override import TestConfigOverride

from src.tests.utils.test_categories import TestUtilsCategories
from src.tests.utils.test_request import TestUtilsRequest

from src.tests.imagesource.t_imgsrc_class import TestImagesourceClass
from src.tests.imagesource.t_imgsrc_dockerhub import TestImagesourceDockerHub

from src.tests.reposource.t_reposrc_class import TestReposourceClass
from src.tests.reposource.t_reposrc_github import TestReposourceGithub


if __name__ == "__main__":
    suites = []
    for suite in [
        TestRepoClass,

        TestConfig,
        TestConfigOverride,

        TestUtilsCategories,
        TestUtilsRequest,

        TestImagesourceClass,
        TestImagesourceDockerHub,

        TestReposourceClass,
        TestReposourceGithub
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()