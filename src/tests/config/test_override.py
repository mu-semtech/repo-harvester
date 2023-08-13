import unittest

from os import remove, path
from ..helpers import test_file_at
from ...repo_harvester.config.overrides import _override_repo_values, apply_overrides
from ...repo_harvester.Category import Category
from ...repo_harvester.config.read_conf_file import CONFIG_DIR

before_change = "before-change"
after_change = "after-change"



class RepoLikeClass():
    def __init__(self, name: str, category: Category=None) -> None:
        self.name = name
        self.imagename = before_change
        self.category = category

test_category = Category("Test", "test")

categories = {
    "test": test_category,
    "archive": Category("Archive", "archive")
}


config_data = """
[mu-cli]
ImageName=mu-cli

[other-repo]
Category=archive


[mu-.*]
Category=test
"""

overrides_conf = CONFIG_DIR.joinpath("overrides.conf")


class TestConfigOverride(unittest.TestCase):

    
    def setUp(self) -> None:
        self.repo = RepoLikeClass("mu-cli")

    def tearDown(self) -> None:
        self.repo = None
    
    
    def test_override_repo_values(self):
        repo = self.repo
        self.assertEqual(repo.imagename, before_change)
        self.assertIsNone(repo.category)

        repo = _override_repo_values(self.repo, {
            "imagename": after_change,
            "category": "Test",
            },
            categories={
                "Test": test_category
            })
        
        self.assertEqual(repo.imagename, after_change)
        self.assertEqual(repo.category, test_category)
    
    def test_override_repo_values_invalid_category(self):
        self.assertRaises(
            KeyError, 
            _override_repo_values,
            self.repo, { "category": "Non-Existant"}
            )
    
    def test_apply_overrides(self):
        test_file_at(overrides_conf, config_data)


        repo_mu_cli = self.repo
        repo_mu_project = RepoLikeClass("mu-project")
        repo_other = RepoLikeClass("other-repo")

        for repo in [repo_mu_cli, repo_mu_project, repo_other]:
            self.assertIsNone(repo.category)
            self.assertEqual(repo.imagename, "before-change")
        

        repo_mu_cli = apply_overrides(repo_mu_cli, categories=categories)
        repo_mu_project = apply_overrides(repo_mu_project, categories=categories)
        repo_other = apply_overrides(repo_other, categories=categories)


        self.assertEqual(repo_mu_cli.category, categories["test"])
        self.assertEqual(repo_other.category, categories["archive"])
        self.assertEqual(repo_mu_project.category, categories["test"])
        
        self.assertEqual(repo_mu_cli.imagename, "mu-cli")
        self.assertEqual(repo_other.imagename, "before-change")
        self.assertEqual(repo_mu_project.imagename, "before-change")

        remove(overrides_conf)
        

if __name__ == "__main__":
    unittest.main()