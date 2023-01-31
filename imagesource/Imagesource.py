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
    
    def get_image_for_repo(self, repo: object):
        for image in self.images:
            print(f"{image.name.lower()} == {repo.name.lower()}")
            if image.name.lower() == repo.name.lower():
                return image
        return next(image for image in self.images if image.name.lower() == repo.name.lower())


class Image():
    """
    A Repo can have multiple images, and are attached as so
    """
    def __init__(self, name: str, image_url: str) -> None:
        self.name = name
        self.image_url = image_url
