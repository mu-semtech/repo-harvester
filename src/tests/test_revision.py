import unittest

from ..app.Revision import Revision

from ..app.utils.request import TMP_REPOHARVESTER
from .helpers import test_file_at

test_data_dir = TMP_REPOHARVESTER + "revision/"


class TestRevisionClass(unittest.TestCase):
    def test_image_and_repo_info(self):
        image_tag = "1.10.1"
        image_url = "https://example.com/image"
        repo_tag = "v1.10.1"
        repo_url = "https://example.com/repo"
        revision = Revision(image_tag, image_url, repo_tag, repo_url, None)
        self.assertEqual(image_tag, revision.image_tag)
        self.assertEqual(image_url, revision.image_url)
        self.assertEqual(repo_tag, revision.repo_tag)
        self.assertEqual(repo_url, revision.repo_url)
        

    def test_docs(self):
        test_file_at(test_data_dir + "README.md", "### Tutorials\nContent")
        test_file_at(test_data_dir + "data/tutorials.md", "# Extra\nGuides")

        revision = Revision("","","","", path_to_repo=test_data_dir)

        self.assertEqual(revision.docs.tutorials.get("README.md"),"# Tutorials\nContent")
        self.assertEqual(revision.docs.tutorials.get("data/tutorials.md"),"# Extra\nGuides")



if __name__ == "__main__":
    unittest.main()