from time import sleep
from ..utils.request import json
from .Imagesource import Imagesource, Image

"""Defines the DockerHub Reposource subclass. All DockerHub API code should be contained in this file."""


class DockerHub(Imagesource):
    def __init__(self, owner: str) -> None:
        super().__init__()
        self.owner = owner
        self.images = []

        images_data = self.get_all_images()
        for image in images_data:
            self.add_image(image_json=image)

    def url_generator(self, image: Image, version: str=None):
        """Override implementation: see Imagesource for more info"""
        return "https://registry.hub.docker.com/r/{0}/{1}/tags".format(
            self.owner, image.name
        )
    
    def add_image(self, image_json: dict):
        """From a DockerHub API object, create a Repo object and add it to to self.repos"""
        if image_json["name"] == "login-service":
            return
        image = Image(
            name=image_json["name"],
            url=self.get_image_url(image_json["name"]),
            imagesource=self)

        tags_array = json(f"https://hub.docker.com/v2/repositories/{self.owner}/{image.name}/tags?page_size=1000", 5)["results"]
        for tag_object in tags_array:
            image.tags.append(tag_object["name"])

        self.images.append(image)
    
    def get_image_url(self, image_name=""):
        """Returns the URL to the image of provided name"""
        return f"https://hub.docker.com/r/{self.owner}/{image_name}"
    
    def get_all_images(self, max_results=100):
        """Return all images from this source"""
        all_images = json(f"https://hub.docker.com/v2/repositories/{self.owner}/?page_size={max_results}")
        return all_images["results"]
    
