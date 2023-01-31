from typing import Any, List
from request import json
from reposource.Reposource import Reposource
from overrides import override_repo_values

class Repo():
    """
    This class holds repository data that we want to export,
    as well as functions to get contents from the repository in question
    """
    def __init__(self, name: str, repo_url: str, homepage_url: str, reposource: Reposource, category_data: Any, other_data: Any) -> None:
        self.name = name
        self.imagename = name

        self.tags : List[Tag] = []

        self.repo_url = repo_url
        self.homepage_url = homepage_url
        
        self.reposource = reposource

        self.category = self.reposource.parse_category(category_data)
        #self.url = json["html_url"]

        # Data of any kind, in case it is needed
        self.other_data = other_data

        self = override_repo_values(self)
    
    @property
    def image(self):
        return self.reposource.imagesource.get_image_by_name(self.imagename)
    
    @property
    def revisions(self):
        revisions_list = []

        image = self.image
        for tag in self.tags:
            if tag.lstrip("v").lstrip("V") in image.tags:
                revisions_list.append(tag)
        
        print("Revisions: " + str(revisions_list))
        return revisions_list

    
    def get_file_url(self, filename):
        return self.reposource.file_url_generator(self, filename)
    
    def get_file_contents(self, path):
        """Request a file, appending the repo url if needed"""
        if "http" not in path.lower():
            path = self.get_file_url(path)
        return json(path)
    
    @property
    def readme(self):
        """Returns the contents of the repository's README"""
        return self.get_file_contents("README.md")
    
    def __str__(self) -> str:
        return f"{self.name}@{self.repo_url}"
    
    def __repr__(self) -> str:
        return self.__str__()


