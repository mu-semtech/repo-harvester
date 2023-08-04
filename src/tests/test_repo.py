import unittest

from os import remove, path
from ..app.imagesource.Imagesource import Imagesource, Image
from ..app.reposource.Reposource import Reposource
from ..app.Repo import Repo
from ..app.Category import Category
from ..app.utils.request import _url_to_cachefile_path
from .helpers import test_file_at
from shutil import rmtree


def test_file_url_generator(repo: object, filename, version=None):
    if not version:
        return f"https://example.com/{repo.name}/{filename}"
    else:
        return f"https://example.com/{repo.name}/{version}/{filename}"

test_imagesource = Imagesource()
test_reposource = Reposource(test_imagesource)
test_reposource.url_generator = lambda version: f"https://example.com/{version}/"
test_reposource.file_url_generator = test_file_url_generator

test_projectname = "parser"
test_image = Image(test_projectname, "https://example.com/", test_imagesource)


test_imagesource.images.append(test_image)





class TestRepoClass(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = Repo(
            reposource=test_reposource,
            name=test_projectname)
        self.repo_without_image = Repo(
            reposource=test_reposource,
            name="parser-2"
        )

    def tearDown(self) -> None:
        pass


    def test_local_dir(self):
        self.assertEqual(
            self.repo.local_dir,
            "/tmp/repo-harvester/parser/"
            )
    
    def test_clone_files(self):
        repo = self.repo

        self.assertFalse(path.exists(repo.local_dir))
        repo.repo_url = "https://github.com/mu-semtech/mu-cl-resources"
        repo.clone_files()
        self.assertTrue(path.exists(repo.local_dir))

        rmtree(repo.local_dir)
    

    
    def test_get_file_url(self):
        self.assertEqual(
            self.repo.get_file_path("README.md"),
            "https://example.com/parser/README.md")
    
    def test_get_file_url_param_version(self):
        self.assertEqual(
            self.repo.get_file_path("README.md", "v0.0.1"),
            "https://example.com/parser/v0.0.1/README.md")
    
    def test_get_file_contents(self):
        test_file_location = _url_to_cachefile_path("https://example.com/parser/README.md")
        test_file_at(test_file_location, "Content")

        self.assertEqual(
            self.repo.get_file_contents("README.md", cache=True),
            "Content")
        
        remove(test_file_location)

    def test_get_file_contents_param_version(self):
        test_file_location = _url_to_cachefile_path("https://example.com/parser/v0.0.1/README.md")
        test_file_at(test_file_location, "Content")

        self.assertEqual(
            self.repo.get_file_contents("README.md", "v0.0.1", cache=True),
            "Content")
        
        remove(test_file_location)

    
    def test_get_file_contents_external_path(self):
        content = self.repo.get_file_contents("https://google.com")
        self.assertTrue(content.lower().startswith("<!doctype html>"))
        self.assertTrue(content.lower().endswith("</html>"))



    def test_prop_image(self):
        self.assertEqual(self.repo.image, test_image)
        self.assertIsNone(self.repo_without_image.image)




if __name__ == "__main__":
    unittest.main()