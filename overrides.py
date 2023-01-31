from configparser import ConfigParser
from re import search, IGNORECASE

from categories import categories

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
