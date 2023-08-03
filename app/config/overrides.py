# Native imports
from re import search, IGNORECASE
# Relative imports
from .conf import read_config
from ..Category import categories
# Package imports
from helpers import log

"""
Code to handle overrides
- Reads the defined overrides from overrides.conf
- Exports a function to apply relevant overrides to a Repo object
"""

config = read_config("overrides")

def override_repo_values(repo: object):
    try: 
        log(config.sections())
        repo_override = config[next(override for override in config.sections() if search(override, repo.name, IGNORECASE))]

        log(repo_override)
        if "imagename" in repo_override:
            repo.imagename = repo_override["imagename"]
            log(f"[OVERRIDE] imagename={repo.imagename}")
        
        if "category" in repo_override:
            repo.category = categories[repo_override["category"]]
            log(f"[OVERRIDE] category={repo.category}")
        
        exit(0)
        
    except StopIteration:
        pass
        exit(1)
    finally:
        return repo