import unittest

from os import remove, path
from ...app.imagesource.DockerHub import DockerHub
from ...app.reposource.GitHub import GitHub
from ...app.Category import Category
from ...app.utils.request import json, contents, request
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
        
    
    def test_url_generator(self):
        repo = github.repo_from_api(template_repo_json)
        self.assertEqual(request(github.url_generator(repo)).status_code, 200)
        self.assertEqual(request(github.url_generator(repo, repo.tags[0])).status_code, 200)

        self.assertNotEqual(request(github.url_generator(repo, "nonexistant")).status_code, 200)

    
    def test_repo_from_api(self):
        
        archived_repo = github.repo_from_api(archived_repo_json, test_categories)
        ember_repo = github.repo_from_api(ember_repo_json, test_categories)
        template_repo = github.repo_from_api(template_repo_json, test_categories)


        self.assertEqual(archived_repo.category, test_categories["archive"])
        self.assertEqual(ember_repo.category, test_categories["ember"])
        self.assertEqual(template_repo.category, test_categories["template"])

        self.assertGreaterEqual(len(archived_repo.tags), 1)
        self.assertGreaterEqual(len(ember_repo.tags), 28)
        self.assertGreaterEqual(len(template_repo.tags), 3)


        self.assertIsNone(archived_repo.homepage_url)
        self.assertIsNotNone(ember_repo.homepage_url)
        self.assertIsNone(template_repo.homepage_url)



        for repo in [archived_repo, ember_repo, template_repo]:
            self.assertIsNotNone(repo.name)
            self.assertIsNotNone(repo.description)
            self.assertTrue("<!doctype html>" in contents(repo.repo_url, cache=True).lower())

    
    def test_get_all_repo_data(self):
        repos_data = github.get_all_repo_data()
        self.assertGreaterEqual(len(repos_data), 50)
        for repo_data in repos_data:
            self.assertIsNotNone(github.repo_from_api(repo_data, categories=test_categories))

if __name__ == "__main__":
    unittest.main()