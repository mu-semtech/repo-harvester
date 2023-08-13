from typing import Dict
from ..Category import Category
from ..config.conf import read_config
from ..utils.log import log

"""
categories defines the categories to use throughout repo-harvester

- Sort by override, then specific regex
- Regex & category names below are based on mu-semtech naming conventions
"""

def _load_categories_from_config(filename="categories") -> Dict[str, Category]:
    config = read_config(filename)

    categories = {}
    for section_name in config.sections():
        section = config[section_name]
        category = Category(section.get("name"), section.get("id"))
        if "regex" in section:
            category.regex = section["regex"]
        
        categories[section_name] = category
    
    return categories


categories = _load_categories_from_config()


def sort_into_category_dict(repos: list) -> dict:
    """A function that turns a List[Repo] into a dict[category_id] = List[Repo]"""
    dict_category_repos = {}
    for category_id in categories:
        if category_id == categories["archive"].id:
            log("INFO", "Skipping archive!")
            continue
        
        category = categories[category_id]
        category_repos = [repo for repo in repos if repo.category.id == category_id]

        dict_category_repos[category.name] = category_repos
    
    return dict_category_repos
