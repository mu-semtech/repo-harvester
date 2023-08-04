import unittest

from os import remove, path
from ...app.Category import Category
from ...app.utils.categories import _load_categories_from_config
from ..helpers import test_file_at

test_file_path = "test.conf"
test_file_content = """
[templates]
name=Templates
id=templates
regex=.*-template
"""

test_file_category = Category("Templates", "templates", ".*-template")


class TestUtilsCategories(unittest.TestCase):

    def setUp(self) -> None:
        test_file_at(test_file_path, test_file_content)

    def tearDown(self) -> None:
        remove(test_file_path)

    
    def test_load_categories_from_config(self):
        categories = _load_categories_from_config(test_file_path)

        self.assertEqual(categories["templates"].name, test_file_category.name)
        self.assertEqual(categories["templates"].id, test_file_category.id)
        self.assertEqual(categories["templates"].regex, test_file_category.regex)



if __name__ == "__main__":
    unittest.main()