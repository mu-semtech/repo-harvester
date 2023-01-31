from configparser import ConfigParser
from re import search, IGNORECASE

from categories import categories

config = ConfigParser()
config.read("overrides.conf")



# This for repos not to be included in docs, and/or repos that break the naming conventions
overrides = {
    r"mu-cli": categories["tools"],
    r"mu-cl-support": categories["archive"],
    r"site-.*": categories["archive"],
    r"presentation-.*": categories["archive"],
}

override_sections = list(config.sections())

def override_repo_values(repo: object):
    try: 
        repo_override = config[next(override for override in config.sections() if search(override, repo.name, IGNORECASE))]

        imagename = repo_override["imagename"]
        if imagename:
            repo.imagename = imagename

        
    except StopIteration:
        pass
    finally:
        return repo
    return
    for override in overrides:
        if search(override, data["name"], IGNORECASE):
            return overrides[override]

