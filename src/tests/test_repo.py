import unittest

from os import remove, path
from ..app.imagesource.Imagesource import Imagesource, Image
from ..app.reposource.Reposource import Reposource
from ..app.Repo import Repo
from ..app.Category import Category
from ..app.utils.request import _url_to_cachefile_path, contents
from .helpers import test_file_at
from shutil import rmtree
from divio_docs_parser import DivioDocs


def test_file_url_generator(repo: object, filename, version=None):
    if not version:
        return f"https://example.com/{repo.name}/{filename}"
    else:
        return f"https://example.com/{repo.name}/{version}/{filename}"

test_imagesource = Imagesource()
test_imagesource.url_generator = lambda x: "https://hub.docker.com/r/semtech/mu-cl-resources"
test_reposource = Reposource(test_imagesource)
test_reposource.url_generator = lambda repo, version: f"https://example.com/{version}/"
test_reposource.file_url_generator = test_file_url_generator

test_projectname = "mu-cl-resources"
test_image = Image(test_projectname, "https://example.com/", test_imagesource)
test_image.tags = ["latest", "1.22.1", "1.17.1", "1.10.2"] 

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

    def test_clone_files(self):
        repo = self.repo
        rmtree(repo.local_dir, ignore_errors=True)

        self.assertFalse(path.exists(repo.local_dir))
        repo.clone_files()
        self.assertTrue(path.exists(repo.local_dir))



    def test_local_dir(self):
        self.assertEqual(
            str(self.repo.local_dir),
            "/tmp/repo-harvester/mu-cl-resources"
            )
        
    def test_tags(self):
        for tag in [TAG_WITHOUT_README, TAG_OLD_README]: 
            self.assertTrue(tag in self.repo.tags)

    
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
        contents_from_github_from_version = contents(f"https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/{version}/README.md", cache=True)
        contents_from_github_from_master = contents("https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/master/README.md", cache=True)

        contents_from_repo = self.repo.get_file_contents("README.md", version)

        self.assertEqual(
            contents_from_repo,
            contents_from_github_from_version
            )
        self.assertNotEqual(
            contents_from_repo,
            contents_from_github_from_master)
        
        self.assertIsNone(self.repo.get_file_contents(
            "README.md", TAG_WITHOUT_README))
        

    def test_prop_image(self):
        self.assertEqual(self.repo.image, test_image)
        self.assertIsNone(self.repo_without_image.image)


    def test_revisions(self):
        revisions = self.repo.revisions()
        self.assertEqual(len(revisions), 3)
        
        tag_to_test = "v1.22.1"

        revision = [revision for revision in revisions if revision.repo_tag == tag_to_test][0]

        docs_from_github = contents(f"https://raw.githubusercontent.com/mu-semtech/mu-cl-resources/{tag_to_test}/README.md", cache=True)
        self.assertEqual(DivioDocs(docs_from_github).tutorials.get("README.md"),
                         revision.docs.tutorials.get("README.md"))


if __name__ == "__main__":
    unittest.main()