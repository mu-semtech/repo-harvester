from re import search, IGNORECASE
from requests import get



def _parse_category_from_name(name):
    """When given a name, use regex to determine the category"""
    for key in categories:
        category = categories[key]
        if category.check_by_name(name):
            return category
    # Fallback
    return categories["tools"]


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


"""
The repo class parses the raw GitHub data
to the data that is relevant for docs generation
"""
class Repo():
    def __init__(self, json) -> None:
        self.name = json["name"]
        self.category = parse_category(json)
        self.url = json["html_url"]

        # Needed for GitHub's file_url_generator specifically
        self.full_name = json["full_name"]
        self.default_branch =json["default_branch"]
    
    def get_file_url(self, filename):
        return github.file_url_generator(self, filename)
    
    def get_file(self, path):
        """Request a file, appending the repo url if needed"""
        if "http" not in path.lower():
            path = self.get_file_url(path)
        return get(path)
    
    @property
    def readme(self):
        return self.get_file("README.md")
    
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