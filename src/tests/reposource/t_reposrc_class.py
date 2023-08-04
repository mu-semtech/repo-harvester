import unittest

from os import remove, path
from ...app.reposource.Reposource import Reposource
from ..helpers import test_file_at


class TestReposourceClass(unittest.TestCase):

    def setUp(self) -> None:
        self.reposource = Reposource(imagesource=None)

    def tearDown(self) -> None:
        self.reposource = None
    
    def test_parse_category_from_name(self):
        return
        
        

if __name__ == "__main__":
    unittest.main()