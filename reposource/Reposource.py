from re import search, IGNORECASE
from typing import Union, Any
from categories import categories, Category
from imagesource.Imagesource import Imagesource

class Reposource():
    """
    A source for one or more repositories. 
    This encompasses:
    - The host (e.g. GitHub, Gitea)
    - Any info that is needed to find the repository (e.g. th owner in github.com/{owner}/{reponame})
    - Code to (if possible) determine the :class:`Category` id
    
    """
    def __init__(self, imagesource: Imagesource) -> None:
        self.repos = []
        self.imagesource = imagesource
    
    def parse_category(self, data: Any) -> Category:
        """
        This function leverages other internal functions to 
        determine the category of a repo.

        This will be used when creating a Repo object.
        """
        
        #for override in overrides:
         #   if search(override, data["name"], IGNORECASE):
          #      return overrides[override]

        category = self._parse_category(data)
        if category != None:
            return category

        else:
            return self._parse_category_from_name(data["name"])  # TODO, this should be replaced
    
    def file_url_generator(self, filename) -> str:
        """
        When given a filename string (e.g. "README.md"), return the full, absolute path towards it.

        *This is a function that should be overridden.*
        """
        pass
    
    def _parse_category(self, data) -> Union[Category, None]:
        """
        When given a parameter, return either: 
        - The name of the category,
          based on data from the Reposource and/or repo
        - None

        *This is a function that should be overridden.*
        """
        return None
    
    def _parse_category_from_name(self, name: str):
        """
        This internal function will be used when no category has been explicitly defined.
        When given a name string, use regex to determine the category.

        It is also the same across every Reposource!
        """
        for key in categories:
            category = categories[key]
            if category.matches_string(name):
                return category
        # Fallback
        return categories["tools"]  # TODO better fallback configuration
