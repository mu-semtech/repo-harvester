class Imagesource():
    """
    A class that is very similar to Reposource,
    containg information about the container host
    (docker hub for example)
    
    This will be used by the Reposource class,
    to be passed to the Repo, so that the Repo
    can use get_images_for_repo!
    """
    def __init__(self) -> None:
        self.images = []
    
    def get_image_by_name(self, name: str):
        for image in self.images:
            print(f"{image.name.lower()} == {name.lower()}")
            if image.name.lower() == name.lower():
                return image
        return False

class Image():
    """
    A Repo can have multiple images, and are attached as so
    """
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url
    
    def __str__(self) -> str:
        return f"{self.name}@{self.url}"
    
    def __repr__(self) -> str:
        return self.__str__()
