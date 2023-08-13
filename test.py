import unittest

from src.tests.test_repo import TestRepoClass
from src.tests.test_revision import TestRevisionClass

from src.tests.config.test_read_config_file import TestConfig
from src.tests.config.test_override import TestConfigOverride
from src.tests.config.test_categories import TestConfigCategories

from src.tests.utils.test_request import TestUtilsRequest

from src.tests.imagesource.t_imgsrc_class import TestImagesourceClass
from src.tests.imagesource.t_imgsrc_dockerhub import TestImagesourceDockerHub

from src.tests.reposource.t_reposrc_class import TestReposourceClass
from src.tests.reposource.t_reposrc_github import TestReposourceGithub

from src.tests.test_index import TestIndex

if __name__ == "__main__":
    suites = []
    for suite in [
        TestRepoClass,
        TestRevisionClass,

        TestConfig,
        TestConfigOverride,
        TestConfigCategories,

        TestUtilsRequest,

        TestImagesourceClass,
        TestImagesourceDockerHub,

        TestReposourceClass,
        TestReposourceGithub,

        TestIndex
    ]:
        suites.append(unittest.makeSuite(suite))

    testSuite = unittest.TestSuite(suites)
    testSuite.run()