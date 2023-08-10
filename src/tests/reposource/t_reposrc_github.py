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



archived_repo_json = json("https://api.github.com/repos/mu-semtech/ember-mu-authorization", cache=True)
ember_repo_json = json("https://api.github.com/repos/mu-semtech/ember-data-table", cache=True)
template_repo_json = json("https://api.github.com/repos/mu-semtech/mu-python-template", cache=True)


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
        
        archived_repo = github.repo_from_api(archived_repo_json, test_categories)
        ember_repo = github.repo_from_api(ember_repo_json, test_categories)
        template_repo = github.repo_from_api(template_repo_json, test_categories)


        self.assertEqual(archived_repo.category, test_categories["archive"])
        self.assertEqual(ember_repo.category, test_categories["ember"])
        self.assertEqual(template_repo.category, test_categories["template"])
    
if __name__ == "__main__":
    unittest.main()