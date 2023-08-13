# Native imports
from typing import Dict
from re import search, IGNORECASE
from configparser import ConfigParser
# Relative imports
from ..Category import Category
from .conf import read_config
from ..utils.categories import categories
# Package imports
try:
    from helpers import log
except ModuleNotFoundError:
    log = print

"""
Code to handle overrides
- Reads the defined overrides from overrides.conf
- Exports a function to apply relevant overrides to a Repo object
"""

def apply_overrides(repo: object, categories:Dict[str, Category]=categories, config_path="overrides"):
    config = read_config(config_path)

    overrides = [override for override in config.sections() if search(override, repo.name, IGNORECASE)]
    
    for override in overrides:
        repo = override_repo_values(repo, config[override], categories)
    
    return repo


def override_repo_values(repo: object, changes:dict, categories:Dict[str, Category]=categories) -> object:
    if "imagename" in changes:
        repo.imagename = changes["imagename"]
        log(f"[OVERRIDE] imagename={repo.imagename}")
    
    if "category" in changes:
        category_id = changes["category"]
        category = None

        try:
            category = categories[category_id]
        except KeyError as error:
            log(f"[OVERRIDE] Category {category_id} doesn't exist!")
            raise error

        if category:
            repo.category = category


        log(f"[OVERRIDE] category={repo.category}")


    return repo
