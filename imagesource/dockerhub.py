from time import sleep
from requests import get
from request import json
from imagesource.Imagesource import Imagesource, Image

class DockerHub(Imagesource):
    def __init__(self, owner: str) -> None:
        super().__init__()
        self.owner = owner
        self.images = []

        images_data = self.get_all_images()
        for image in images_data:
            self.add_image(image_json=image)

    
    def add_image(self, image_json: dict):
        if image_json["name"] == "login-service":
            return
        image = Image(
            name=image_json["name"],
            url=self.get_image_url(image_json["name"]))

        tags_array = json(f"https://hub.docker.com/v2/repositories/{self.owner}/{image.name}/tags?page_size=1000", 5)["results"]
        for tag_object in tags_array:
            image.tags.append(tag_object["name"])

        self.images.append(image)
    
    def get_image_url(self, image_name=""):
        return f"https://hub.docker.com/r/{self.owner}/{image_name}"
    
    def get_all_images(self, max_results=100):
        request = get(f"https://hub.docker.com/v2/repositories/{self.owner}/?page_size={max_results}")
        return request.json()["results"]
    
