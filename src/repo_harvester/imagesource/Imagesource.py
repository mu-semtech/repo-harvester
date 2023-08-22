"""Defines the Imagesource base class, as well as the Image class"""

class Imagesource():
    """
    A class that is very similar to Reposource, containg information about the container image host
    For example: DockerHub

    self.images should be populated with Image objects
    
    This will be used by the Reposource class, to be passed to the Repo, so that the Repo can use get_images_for_repo
    """
    def __init__(self) -> None:
        self.images = []

    def url_generator(self, version=None) -> str:
        """
        When given a version (e.g. main, master, v1.1, c23a3ef...) return the URL to that release/tag/commit

        *This is a function that should be overridden.*
        """
        pass
    
    def get_image_by_name(self, name: str):
        """From self.images, find the image with the provided name"""
        for image in self.images:
            if image is None:
                continue  # TODO why is there None?
            if image.name.lower() == name.lower():
                return image
        return None

    def load_images(self):
        """
        When run - even without parameters - all images should be automatically loaded into self.images

        *This is a function that should be overridden.*
        """
        pass


class Image():
    """Class to contain all Image data. Note that a Repo can have multiple images."""
    def __init__(self, name: str, url: str, imagesource: Imagesource) -> None:
        self.name = name
        self.url = url
        self.tags = []
        self.imagesource = imagesource
    
    def get_image_tag_if_exists(self, needle: str):
        try:
            return next(filter(lambda image_tag: image_tag.lower() == needle.lower(), self.tags))
        except StopIteration:
            return None
    
    def __str__(self) -> str:
        return f"{self.name}@{self.url}"
    
    def __repr__(self) -> str:
        return self.__str__()
