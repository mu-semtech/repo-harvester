from re import search, IGNORECASE
from .config.conf import read_config
try:
    from helpers import log
except ModuleNotFoundError:
    log = print
"""
All code relevant to categories:
- Category class 
- The dict defining the categories to be used
- Any helper functions

For information on what categories are, see the relevant README discussion.
"""

class Category():
    """
    The Category a Repo belongs to.
    This is an abstract, self definable thing,
    referring to how *you* would like to sort and categorise the repository
    """
    def __init__(self, name, id, regex=""):
        self.name = name
        self.id = id
        self.regex = regex
    
    @property
    def url(self):
        """Return a linked data URL for the category"""
        return f"http://mu.semte.ch/vocabularies/ext/category/{self.id}"
    
    def matches_string(self, string: str):
        """If the category has a regex pattern, check if the provided string matches it"""
        if self.regex:
            return search(self.regex, string, IGNORECASE)
        else:
            return None
    
    def __str__(self) -> str:
        return f"{self.id}:{self.name} - {self.regex}" 
    
    def __repr__(self) -> str:
        return self.__str__()

