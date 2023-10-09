"""Code to handle Repo overrides (e.g. set to a specific category, change image name...)"""

# Built-in imports
from typing import Dict
from re import search, IGNORECASE

# Relative imports
from . import read_config, categories_from_conf
from ..Category import Category
from ..utils import log


def apply_overrides(repo: object, categories:Dict[str, Category]=categories_from_conf, config_path="overrides"):
    """
    When passed a repo object, return it with the needed properties overrided

    Optional parameters:
    - categories: dictionary of categories to use when overriding. Defaults to the categories defined in config/categories.conf
    - config_path: the name of the conf file containing the overrides to pass to read_config. Defaults to overrides 
    """
    config = read_config(config_path)

    overrides = [override for override in config.sections() if search(override, repo.name, IGNORECASE)]
    
    for override in overrides:
        log("INFO", f"OVERRIDE: {repo.name} - {override} - {config[override]}")
        repo = _override_repo_values(repo, config[override], categories)
    
    return repo


def _override_repo_values(repo: object, changes:dict, categories:Dict[str, Category]=categories_from_conf) -> object:
    """
    Override a single repo's properties with all the changes defines in the `changes` dict parameter.

    Optional parameter:
    - categories: dictionary of categories to use when overriding. Defaults to the categories defined in config/categories.conf
    """

    if "imagename" in changes:
        repo.imagename = changes["imagename"]
        log("INFO", f"[OVERRIDE] imagename={repo.imagename}")
    
    if "category" in changes:
        category_id = changes["category"]
        category = None

        try:
            category = categories[category_id]
        except KeyError as error:
            log("INFO", f"[OVERRIDE] Category {category_id} doesn't exist!")
            raise error

        if category:
            repo.category = category


        log("INFO", f"[OVERRIDE] category={repo.category}")


    return repo
