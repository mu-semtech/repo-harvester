import unittest

from os import remove, path
#from ..app.config.conf import read_config, CONFIG_PATH
from .helpers import test_file_at
from ..app.config.overrides import override_repo_values
from ..app.Category import Category

before_change = "before-change"
after_change = "after-change"



class RepoLikeClass():
    def __init__(self) -> None:
        self.name = "mu-cli"
        self.imagename = before_change
        self.category = None

test_category = Category("Test", "test")

class TestConfigOverride(unittest.TestCase):

    
    def setUp(self) -> None:
        self.repo = RepoLikeClass()

    def tearDown(self) -> None:
        self.repo = None
    
    
    def test_override_repo_values(self):
        repo = self.repo
        self.assertEqual(repo.imagename, before_change)
        self.assertIsNone(repo.category)

        repo = override_repo_values(self.repo, {
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
            override_repo_values,
            self.repo, { "category": "Non-Existant"}
            )
        

if __name__ == "__main__":
    unittest.main()