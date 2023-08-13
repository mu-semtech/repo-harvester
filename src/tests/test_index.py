import unittest

from os import remove

from ..app.index import load_repos_from, load_repos_from_config
from ..app.Category import Category
from ..app.imagesource.Imagesource import Imagesource
from ..app.imagesource.DockerHub import DockerHub
from ..app.reposource.Reposource import Reposource
from ..app.reposource.GitHub import GitHub

from .helpers import test_file_at

test_categories = {
    "template": Category("Templates", "template", ".*-template"),
    "ember": Category("Ember addons", "ember", "ember-.*"),
    "tools": Category("Tools", "tool"),
    "archive": Category("Archive", "archive")
}


class TestIndex(unittest.TestCase):
    def test_load_repos_from(self):
        repos = load_repos_from(
            reposource=GitHub,
            repos_username="mu-semtech",
            imagesource=DockerHub,
            images_username="semtech",
            categories=test_categories
        )

        self.assertGreaterEqual(len(repos), 50)
    

    def test_load_repos_from_config(self):
        test_conf = "test.conf"
        conf_contents = """
[mu-semtech GitHub + DockerHub]
repos_host=GitHub
repos_username=mu-semtech
images_host=DockerHub
images_username=semtech
"""
        test_file_at(test_conf, conf_contents)

        repos = load_repos_from_config(test_conf, test_categories)

        self.assertGreaterEqual(len(repos), 50)

        remove(test_conf)



if __name__ == "__main__":
    unittest.main()