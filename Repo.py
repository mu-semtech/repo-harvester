from re import search, IGNORECASE
from requests import get
from abc import abstractmethod
from typing import List, Any


class Reposource():
    def __init__(self) -> None:
        self.repos = []
    
    def parse_category(self, data: Any):
        """
        This function leverages other internal functions to 
        determine the category of a repo.

        This will be used when creating a Repo object.
        """
        category = self._parse_category(data=data)
        if category != None:
            return category

        else:  # TODO move override up?
            for override in overrides:
                if search(override, data["name"], IGNORECASE):
                    return overrides[override]
            
            return self._parse_category_from_name(data["name"])  # TODO, this should be replaced
    
    def file_url_generator(self, filename):
        """
        *This is a function that should be overridden.*

        When given a filename (e.g. README.md), return the full, absolute path towards it.
        """
        pass
    
    def _parse_category(self, data):
        """
        This is a function that should be overridden.
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
            if category.check_by_name(name):
                return category
        # Fallback
        return categories["tools"]  # TODO better fallback configuration


class Category():
    def __init__(self, name, id, regex=""):
        self.name = name
        self.id = id
        self.regex = regex
    
    def check_by_name(self, param):
        """If the category has a regex pattern, check it against the provided parameter"""
        if self.regex:
            return search(self.regex, param, IGNORECASE)
        else:
            return None
    
    def __str__(self) -> str:
        return self.name



class Repo():
    """
    The repo class holds data that is relevant to our end goals only
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