"""Defines the DockerHub Imagesource. All DockerHub code - API or otherwise - should be contained in this file."""

# Built-in imports
from typing import List

# Relative imports
from ..utils import json
from ..imagesource import Imagesource, Image


class DockerHub(Imagesource):
    def __init__(self, owner: str) -> None:
        super().__init__()
        self.owner = owner
        """Username to find the images under"""
        self.images: List[Image] = []
        """List of images owned by self.owner. Empty until load_images is called"""


    def url_generator(self, image: Image, version: str=None):
        """Override implementation: see Imagesource for more info"""
        return f"https://registry.hub.docker.com/r/{self.owner}/{image.name}/tags"
    
    def get_image_url(self, image_name: str):
        """Returns the URL to the image of provided name"""
        return f"https://hub.docker.com/r/{self.owner}/{image_name}"
    

    def image_from_api(self, image_json: dict):
        """From a DockerHub API response, create and return an Image object"""
        if image_json["name"] == "login-service":
            return  # TODO
        image = Image(
            name=image_json["name"],
            url=self.get_image_url(image_json["name"]),
            imagesource=self)

        tags_array = json(f"https://hub.docker.com/v2/repositories/{self.owner}/{image.name}/tags?page_size=1000", 5)["results"]
        for tag_object in tags_array:
            image.tags.append(tag_object["name"])

        return image    

    def get_images_data(self, max_results=100) -> object:
        """Return a DockerHub API response containing all images from `self.owner` on DockerHub"""
        # TODO improve implementation
        all_images = json(f"https://hub.docker.com/v2/repositories/{self.owner}/?page_size={max_results}")
        return all_images["results"]

    def load_images(self, max_results=100):
        """When called, load all the images from `self.owner` on DockerHub and loads the Image objects into `self.images`"""
        images_data = self.get_images_data(max_results)
        for image in images_data:
            self.images.append(self.image_from_api(image_json=image))

