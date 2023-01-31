from re import search, IGNORECASE

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
