import unittest

from os import remove, path
from ..app.imagesource.Imagesource import Imagesource, Image
from ..app.reposource.Reposource import Reposource
from ..app.Repo import Repo
from ..app.Category import Category
from ..app.utils.request import _url_to_cachefile_path, contents
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

test_projectname = "mu-cl-resources"
test_image = Image(test_projectname, "https://example.com/", test_imagesource)

TAG_WITHOUT_README = "v1.10.2"
TAG_OLD_README = "v1.17.1"


test_imagesource.images.append(test_image)


repo = Repo(
    reposource=test_reposource,
    name="mu-cl-resources")
repo.repo_url = "https://github.com/mu-semtech/mu-cl-resources.git"
rmtree(repo.local_dir, ignore_errors=True)
repo.clone_files()


class TestRepoClass(unittest.TestCase):

    def setUp(self) -> None:

        self.repo = repo
        self.repo_without_image = Repo(
            reposource=test_reposource,
            name="parser-2"
        )

    def tearDown(self) -> None:
        pass


    def test_local_dir(self):
        self.assertEqual(
            str(self.repo.local_dir),
            "/tmp/repo-harvester/mu-cl-resources"
            )
    
    def test_clone_files(self):
        repo = self.repo
        rmtree(repo.local_dir, ignore_errors=True)

        self.assertFalse(path.exists(repo.local_dir))
        repo.clone_files()
        self.assertTrue(path.exists(repo.local_dir))

        #rmtree(repo.local_dir)
    

    
    def test_get_file_path(self):
        self.assertEqual(
            str(self.repo.get_file_path("README.md")),
            "/tmp/repo-harvester/mu-cl-resources/README.md")
    
    def test_get_file_contents(self):
        readme_contents_from_github = contents("https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/master/README.md")

        self.assertEqual(
            self.repo.get_file_contents("README.md"),
            readme_contents_from_github
            )
    
    def test_get_file_contents_branch(self):
        branch = "overeager-caching-tests"
        file = "framework/call-implementation.lisp"
        contents_from_github_from_branch = contents(f"https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/{branch}/" + file)
        contents_from_github_from_master = contents("https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/master/" + file)

        contents_from_repo = self.repo.get_file_contents(file, branch)

        self.assertEqual(
            contents_from_repo,
            contents_from_github_from_branch
            )
        self.assertNotEqual(
            contents_from_repo,
            contents_from_github_from_master
        )
    
    def test_get_file_contents_tag(self):
        version = TAG_OLD_README
        contents_from_github_from_version = contents(f"https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/{version}/README.md")
        contents_from_github_from_master = contents("https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/master/README.md")

        contents_from_repo = self.repo.get_file_contents("README.md", version)

        self.assertEqual(
            contents_from_repo,
            contents_from_github_from_version
            )
        self.assertNotEqual(
            contents_from_repo,
            contents_from_github_from_master)
        
        self.assertRaises(
            FileNotFoundError, 
            self.repo.get_file_contents, 
            "README.md", 
            TAG_WITHOUT_README)
        

    def test_get_file_contents_param_version(self):
        return
        test_file_location = _url_to_cachefile_path("https://example.com/parser/v0.0.1/README.md")
        test_file_at(test_file_location, "Content")

        self.assertEqual(
            self.repo.get_file_contents("README.md", "v0.0.1", cache=True),
            "Content")
        
        remove(test_file_location)

    
    def test_get_file_contents_external_path(self):
        return
        content = self.repo.get_file_contents("https://google.com")
        self.assertTrue(content.lower().startswith("<!doctype html>"))
        self.assertTrue(content.lower().endswith("</html>"))



    def test_prop_image(self):
        return
        self.assertEqual(self.repo.image, test_image)
        self.assertIsNone(self.repo_without_image.image)




if __name__ == "__main__":
    unittest.main()