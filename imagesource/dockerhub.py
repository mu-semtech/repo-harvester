from Repo import Imagesource, Image
from requests import get

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
            image_url=self.get_image_url(image_json["name"]))
        self.images.append(image)
    
    def get_image_url(self, image_name=""):
        return f"https://hub.docker.com/r/{self.owner}/{image_name}"
    
    def get_all_images(self, max_results=100):
        request = get(f"https://hub.docker.com/v2/repositories/{self.owner}/?page_size={max_results}")
        return request.json()["results"]
    
