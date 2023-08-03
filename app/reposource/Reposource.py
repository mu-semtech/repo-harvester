# Native imports
from typing import Union, Any
# Relative imports
from ..Category import categories, Category
from ..imagesource.Imagesource import Imagesource

"""Defines the Reposource superclass"""


class Reposource():
    """
    A source for one or more repositories. 

    This encompasses:
    - The host (e.g. GitHub, Gitea) and how to read & interpret data from their API's
    - Any info that is needed to find any relevant repositories
      Usually, this will include the owner of a specific account from which to harvest
    - Code to (if possible) determine the Category

    This class is *not* meant to be called directly. Rather it is meant to be used to subclass Repo sources.
    See GitHub.py for an example
    
    """
    def __init__(self, imagesource: Imagesource) -> None:
        self.repos = []
        self.imagesource = imagesource
    
    def parse_category(self, data: Any) -> Category:
        """
        This function leverages other internal functions to determine the category of a repo.

        This will be used when creating a Repo object.
        """
        
        category = self._parse_category(data)
        if category != None:
            return category

        else:
            return self._parse_category_from_name(data["name"])  # TODO, this should be replaced
    
    def url_generator(self, version=None) -> str:
        """
        When given a version (e.g. main, master, v1.1, c23a3ef...) return the URL to that release/tag/commit's page

        *This is a function that should be overridden.*
        """
        pass

    def file_url_generator(self, filename, version=None) -> str:
        """
        When given a filename string (e.g. "README.md"), return the full, absolute URL towards it.
        When this is optionally passed a version (can be a release tag, branch...), make sure to return that versions'... version

        *This is a function that should be overridden.*
        """
        pass
    
    def _parse_category(self, data: Any) -> Union[Category, None]:
        """
        When given a parameter, return either: 
        - The relevant Category object, based on data from the Reposource and/or Repo
        - None

        This is *not* the place to determine Category using name/regex. That is _parse_category_from_name.
        This *is* the place to determine e.g. Category 'archive' from repo_api_data.is_archived == True

        *This is a function that should be overridden.*
        """
        return None
    
    def _parse_category_from_name(self, name: str):
        """
        This internal function will be used when the category can not be automatically determined through _parse_category.
        When given a name string, use regex to determine the category.

        It is also the same across every Reposource, and does not need to be overriden.
        """
        for key in categories:
            category = categories[key]
            if category.matches_string(name):
                return category
        # Fallback
        return categories["tools"]  # TODO better fallback configuration
