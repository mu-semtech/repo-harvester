"""Collects top-level code for collecting repos"""

# Built-in imports
from typing import List, Dict

# Relative imports
from . import read_config, log, Repo, Imagesource, Reposource, DockerHub, GitHub, categories_from_conf, Category

def load_repos_from(reposource: Reposource, repos_username: str, imagesource: Imagesource, images_username: str, 
                    categories:Dict[str, Category]=categories_from_conf) -> List[Repo]:
    """
    - Creates a reposource & imagesource from the passed classes & username
    - Loads all images
    - Assigns the imagesource to the reposource
    - Loads all repos
    - Return reposource.repos
    """
    imagesource = imagesource(images_username)
    imagesource.load_images()


    reposource = reposource(repos_username, imagesource)
    reposource.load_repos(categories)

    return reposource.repos

def load_repos_from_config(config="repos.conf", categories:Dict[str, Category]=categories_from_conf) -> List[Repo]:
    """Returns a list of all repos that can be found with the Reposource(s) specified in `repos.conf`"""

    log("INFO", f"Loading repos using {config}...")
    repos = []

    config = read_config(config)
    for section_name in config.sections():
        log("INFO", f"Loading section {section_name}")
        section = config[section_name]

        images_username = section.get("images_username")
        repos_username = section.get("repos_username")

        images_host = section.get("images_host").lower()
        repos_host = section.get("repos_host").lower()

        log("INFO", f"Passed config: {images_username} + {images_host}\t|\t{repos_username} + {repos_host}")
        
        # Get Imagesource first, because it has to be added to Reposource
        if images_host == "dockerhub":
            imagesource = DockerHub
        else:
            log("CRITICAL", f"{section_name}'s image_host ({images_host}) does not exist")
            exit()  # TODO error code

        if repos_host == "github":
            reposource = GitHub
        else:
            log("CRITICAL", f"{section_name}'s repos_host ({repos_host}) does not exist")
            exit()
        
        repos += load_repos_from(reposource, repos_username, imagesource, images_username, categories)
    
    log("INFO", "All sections loaded, returning repos")

    return repos
