import unittest

from os import remove, path
from ...app.reposource.Reposource import Reposource
from ...app.Category import Category
from ..helpers import test_file_at

reposource = Reposource(imagesource=None)
test_categories = {
    "template": Category("Templates", "template", ".*-template"),
    "ember": Category("Ember addons", "ember", "ember-.*"),
    "tools": Category("Tools", "tool")
}

class TestReposourceClass(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
    
    def test_parse_category_from_data(self):
        self.assertIsNone(
            reposource._parse_category_from_data({"name": "python-template"}),
            "The base Reposource class should return None for _parse_category_from_data")
        
    def test_parse_category_from_name(self):
        self.assertEqual(
            reposource._parse_category_from_name("python-template", test_categories),
            test_categories["template"])

        self.assertEqual(
            reposource._parse_category_from_name("ember-power-select", test_categories),
            test_categories["ember"])
        
        self.assertEqual(
            reposource._parse_category_from_name("powerpoint", test_categories),
            test_categories["tools"])
    
    def test_parse_category(self):
        self.assertEqual(
            reposource.parse_category({"name": "python-template"}, test_categories),
            test_categories["template"],
            "Due to the base class not having a _parse_category_from_data, the same result as _parse_category_from_name should be given")
    
    def test_url_generator(self):
        self.assertIsNone(
            reposource.url_generator({"name": "python-template"}),
            "The base Reposource class should return None for url_generator")
        
    def test_file_url_generator(self):
        self.assertIsNone(
            reposource.file_url_generator("fileanme"),
            "The base Reposource class should return None for url_generator")
        
if __name__ == "__main__":
    unittest.main()