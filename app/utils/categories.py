from ..Category import Category
from ..config.conf import read_config

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