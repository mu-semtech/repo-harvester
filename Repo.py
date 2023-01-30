from re import search, IGNORECASE
from requests import get
from abc import abstractmethod
from typing import List, Any, Union

class Category():
    """
    The Category a :class:`Repo` belongs to.
    This is an abstract, self definable thing,
    referring to how *you* would like to sort and categorise the repository
    """
    def __init__(self, name, id, regex=""):
        self.name = name
        self.id = id
        self.regex = regex
    
    def matches_string(self, string: str):
        """If the category has a regex pattern, check if the provided parameter matches it"""
        if self.regex:
            return search(self.regex, string, IGNORECASE)
        else:
            return None
    
    def __str__(self) -> str:
        return self.name



class Reposource():
    """
    A source for one or more repositories. 
    This encompasses:
    - The host (e.g. GitHub, Gitea)
    - Any info that is needed to find the repository (e.g. th owner in github.com/{owner}/{reponame})
    - Code to (if possible) determine the :class:`Category` id
    
    """
    def __init__(self) -> None:
        self.repos = []
    
    def parse_category(self, data: Any) -> Category:
        """
        This function leverages other internal functions to 
        determine the category of a repo.

        This will be used when creating a Repo object.
        """
        
        for override in overrides:
            if search(override, data["name"], IGNORECASE):
                return overrides[override]

        category = self._parse_category(data=data)
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



class Repo():
    """
    This class holds repository data that we want to export,
    as well as functions to get contents from the repository in question
    """
    def __init__(self, name: str, reposource: Reposource, category_data: Any, other_data: Any) -> None:
        self.name = name
        self.reposource = reposource
        self.category = self.reposource.parse_category(category_data)
        #self.url = json["html_url"]

        # Data of any kind, in case it is needed
        self.other_data = other_data

        self.reposource.repos.append(self)
    
    def get_file_url(self, filename):
        return self.reposource.file_url_generator(self, filename)
    
    def get_file_contents(self, path):
        """Request a file, appending the repo url if needed"""
        if "http" not in path.lower():
            path = self.get_file_url(path)
        return get(path)
    
    @property
    def readme(self):
        """Returns the contents of the repository's README"""
        return self.get_file_contents("README.md")
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

# Sort by override, then specific regex
# Regex & category names are based on mu-semtech naming conventions
categories = {
    "templates": Category("Templates", "templates", r".*-template"),
    "microservices": Category("Microservices", "microservices", r".*-service"),
    "ember-addons": Category("Ember Addons", "ember-addons", r"ember-.*"),
    "core": Category("Core", "core", r"mu-.*"),
    "archive": Category("Archive", "archive"),  # Ignored
    "tools": Category("Tools", "tools"),
}

# This for repos not to be included in docs, and/or repos that break the naming conventions
overrides = {
    r"mu-cli": categories["tools"],
    r"mu-cl-support": categories["archive"],
    r"site-.*": categories["archive"],
    r"presentation-.*": categories["archive"],
}