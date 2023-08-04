import unittest

from os import remove, path
from ...app.imagesource.DockerHub import DockerHub
from ...app.reposource.GitHub import GitHub
from ...app.Category import Category
from ...app.utils.request import json
from ..helpers import test_file_at


imagesource = DockerHub("semtech")
imagesource.images = imagesource.get_images_data(5)

github = GitHub("mu-semtech", imagesource=imagesource)
test_categories = {
    "template": Category("Templates", "template", ".*-template"),
    "ember": Category("Ember addons", "ember", "ember-.*"),
    "tools": Category("Tools", "tool"),
    "archive": Category("Archive", "archive")
}

class TestReposourceGithub(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
    
    def test_parse_category_from_data(self):
        self.assertIsNone(github._parse_category_from_data({"name": "python-template", "archived": False}, test_categories))
        self.assertEqual(
            github._parse_category_from_data({"name": "python-template", "archived": "True"}, test_categories),
            test_categories["archive"])
    
    def test_parse_category(self):
        self.assertEqual(
            github.parse_category({"name": "python-template", "archived": False}, test_categories),
            test_categories["template"])
            
        self.assertEqual(
            github._parse_category_from_data({"name": "python-template", "archived": "True"}, test_categories),
            test_categories["archive"])
    
    def test_repo_from_api(self):
        repo_json = json("https://api.github.com/repos/mu-semtech/mu-identifier")
        
        repo = github.repo_from_api(repo_json)
    
if __name__ == "__main__":
    unittest.main()