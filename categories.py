from re import search, IGNORECASE
from conf import read_config
from helpers import log
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


"""
categories defines the categories to use throughout repo-harvester

- Sort by override, then specific regex
- Regex & category names below are based on mu-semtech naming conventions
"""
categories = {}

config = read_config("categories")

for section_name in config.sections():
    section = config[section_name]
    category = Category(section.get("name"), section.get("id"))
    if "regex" in section:
        category.regex = section["regex"]
    
    categories[section_name] = category

log(categories)

def sort_into_category_dict(repos: list) -> dict:
    """A function that turns a List[Repo] into a dict[category_id] = List[Repo]"""
    dict_category_repos = {}
    for category_id in categories:
        if category_id == categories["archive"].id:
            print("Skipping archive!")
            continue
        
        category = categories[category_id]
        category_repos = [repo for repo in repos if repo.category.id == category_id]

        dict_category_repos[category.name] = category_repos
    
    return dict_category_repos
