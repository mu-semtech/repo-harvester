import unittest

from os import remove, path
from ...app.imagesource.Imagesource import Image
from ...app.imagesource.DockerHub import DockerHub
from ..helpers import test_file_at


class TestImagesourceDockerHub(unittest.TestCase):

    def setUp(self) -> None:
        self.imagesource = DockerHub("_")  # Docker image account
        self.image = Image("alpine", "https://hub.docker.com/r/_/alpine", self.imagesource)


    def tearDown(self) -> None:
        self.imagesource = None
    
    def test_url_generator(self):
        print(self.imagesource.url_generator(self.image))

       
if __name__ == "__main__":
    unittest.main()