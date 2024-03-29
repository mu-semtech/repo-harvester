"""This file defines the categories dictionary to use throughout the project"""

# Built-in imports
from typing import Dict

# Relative imports
from . import read_config
from ..utils import log
from ..Category import Category


def _load_categories_from_config(filename="categories") -> Dict[str, Category]:
    """
    Reads the .conf file with the passed filename,
    and exports the categories defined within as a dict with the following structure: {category_id: category_object}

    Optional parameters:
    - filename: the filename to pass to read_config. Defaults to categories (e.g. config/categories.conf)
    """
    config = read_config(filename)

    categories = {}
    for section_name in config.sections():
        section = config[section_name]
        category = Category(section.get("name"), section.get("id"))
        if "regex" in section:
            category.regex = section["regex"]
        
        categories[section_name] = category
    
    return categories


categories_from_conf = _load_categories_from_config()
"""The categories loaded from categories.conf as a dict with the following structure: {category_id: category_object}"""


def sort_into_category_dict(repos: list) -> dict:
    """A function that turns a List[Repo] into a dict[category_id] = List[Repo]"""
    dict_category_repos = {}
    for category_id in categories_from_conf:
        if category_id == categories_from_conf["archive"].id:
            log("INFO", "Skipping archive!")
            continue
        
        category = categories_from_conf[category_id]
        category_repos = [repo for repo in repos if repo.category.id == category_id]

        dict_category_repos[category.name] = category_repos
    
    return dict_category_repos
