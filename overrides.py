# Native imports
from re import search, IGNORECASE
from configparser import ConfigParser
# Relative imports
from categories import categories

"""
Code to handle overrides
- Reads the defined overrides from overrides.conf
- Exports a function to apply relevant overrides to a Repo object
"""

config = ConfigParser()
config.read("overrides.conf")

def override_repo_values(repo: object):
    try: 
        repo_override = config[next(override for override in config.sections() if search(override, repo.name, IGNORECASE))]

        if "imagename" in repo_override:
            repo.imagename = repo_override["imagename"]
        
        if "category" in repo_override:
            repo.category = categories[repo_override["category"]]
        
    except StopIteration:
        pass
    finally:
        return repo
