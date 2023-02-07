from typing import Any, List
from request import json, contents
from reposource.Reposource import Reposource
from overrides import override_repo_values

class Revision():
    def __init__(self, image_tag: str, image_url: str, repo_tag: str, repo_url: str, readme: str) -> None:
        self.image_tag = image_tag
        self.image_url = image_url
        self.repo_tag = repo_tag
        self.repo_url = repo_url
        self.readme = readme


class Repo():
    """
    This class holds repository data that we want to export,
    as well as functions to get contents from the repository in question
    """
    def __init__(self, name: str, description: str, repo_url: str, homepage_url: str, reposource: Reposource, category_data: Any, other_data: Any) -> None:
        self.name = name
        self.description = description
        self.imagename = name

        self.tags = []

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
    def revisions(self) -> List[Revision]:
        revisions_list = []

        image = self.image
        for repo_tag in self.tags:
            try:
                stripped_repo_tag = repo_tag.lstrip("v").lstrip("V").lower()
                image_tag = next(filter(lambda image_tag: image_tag.lower() == stripped_repo_tag , image.tags))
                revisions_list.append(Revision(
                    image_tag,
                    "",
                    repo_tag,
                    self.reposource.url_generator(self, repo_tag),
                    self.readme(False, repo_tag)
                ))
            except StopIteration:
                pass  # image_tag not found, pass
        print("Revisions: " + str(revisions_list))
        return revisions_list

    
    def get_file_url(self, filename, version=None):
        return self.reposource.file_url_generator(self, filename, version)
    
    def get_file_contents(self, path, version=None):
        """Request a file, appending the repo url if needed"""
        if "http" not in path.lower():
            path = self.get_file_url(path, version)
        return contents(path)
    
    def readme(self, escaped=False, version=None):
        """Returns the contents of the repository's README"""
        data = self.get_file_contents("README.md", version) 
        if escaped:
                # escape(Markup(
                #.replace("'", "&apos;")
                #.replace("*", "")   
                #))
            data = data\
                .replace("\\", "&bsol;")\
                .replace('"', "&quot;")\
                .replace("\n", "\\n")
        return version
    
    def __str__(self) -> str:
        return f"{self.name}@{self.repo_url}"
    
    def __repr__(self) -> str:
        return self.__str__()


