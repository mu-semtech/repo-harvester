import unittest

from ...app.imagesource.Imagesource import Image
from ...app.utils.request import request, json
from ...app.imagesource.DockerHub import DockerHub


imagesource = DockerHub("bitnami")  # Docker image account


class TestImagesourceDockerHub(unittest.TestCase):

    def setUp(self) -> None:
        self.imagesource = imagesource
        self.image = Image("redis", "https://hub.docker.com/r/bitnami/redis", self.imagesource)

    def tearDown(self) -> None:
        self.imagesource = None
    
    def test_url_generator(self):
        self.assertEqual(
            request("https://nonexistant.github.com").status_code,
            404
        )

        generated_url_request = request(self.imagesource.url_generator(self.image))

        self.assertEqual(
            generated_url_request.status_code,
            200
        )

        for word in ["docker.com", self.imagesource.owner, self.image.name, "tag"]:
            self.assertTrue(word in generated_url_request.url)

    def test_get_image_url(self):
        self.assertEqual(
            self.imagesource.get_image_url("redis"),
            "https://hub.docker.com/r/bitnami/redis"
            )

    def test_image_from_api(self):
        example_image_json = json("https://hub.docker.com/v2/repositories/bitnami/?page_size=1")["results"][0]

        image = self.imagesource.image_from_api(example_image_json)
        self.assertEqual(image.name, "redis")
        self.assertEqual(image.url, "https://hub.docker.com/r/bitnami/redis")
        self.assertTrue("latest" in image.tags)


    def test_get_images_data(self):
        self.assertEqual(
            len(self.imagesource.get_images_data(2)),
            2
        )
    
    def test_load_images(self):
        self.imagesource.load_images(3)
        self.assertEqual(
            len(self.imagesource.images),
            3
        )
        first_image = self.imagesource.images[0]
        self.assertEqual(first_image.name, self.image.name)
        self.assertEqual(first_image.url, self.image.url)
        self.assertEqual(first_image.imagesource, self.image.imagesource)
       
if __name__ == "__main__":
    unittest.main()