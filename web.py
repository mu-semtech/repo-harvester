from src.app.config.conf import read_config
from src.app.reposource.GitHub import GitHub
from src.app.imagesource.DockerHub import DockerHub
from src.app.Category import sort_into_category_dict
from src.app.sparql import add_repos_to_triplestore
from helpers import log

"""
Entrypoint for the repo-harvester:
- Defines endpoints
- Defines repo & image sources

app should not be defined here, as this is handled by mu-python-template
"""


@app.route("/")
def index():
    """Simple status page to check if the repo harvester works"""
    return "Repo harvester online!"

@app.route("/init", methods=["GET", "POST"])
def init():
    """Calls add_repos_to_triplestore with init, initialising the database"""
    return add_repos(init=True)


@app.route("/update", methods=["GET", "POST"])
def update():
    """Calls add_repos_to_triplestore without init, updating the database"""
    return add_repos(init=False)


def add_repos(init=False):
    """Initialise/update the database with repo & image information"""
    
    log("Updating...")
    repos = []

    config = read_config("repos")
    for section_name in config.sections():
        section = config[section_name]
        

        images_username = section.get("images_username")
        repos_username = section.get("repos_username")
        
        # Get Imagesource first, because it has to be added to Reposource
        if section.get("images_host").lower() == "dockerhub":
            imagesource = DockerHub(images_username)
        else:
            imagesource = DockerHub(images_username)

        if section.get("repos_host").lower() == "github":
            reposource = GitHub(repos_username, imagesource)
        else:
            reposource = GitHub(repos_username, imagesource)
        
        repos += reposource.repos
    
    log(repos)

    # Testing stuff
    #dict_category_repos = sort_into_category_dict(mu_semtech_github.repos)
    #repo = mu_semtech_github.repos[8]
    #log(repo)
    #log(repo.description)
    #log(repo.image)
    #log(repo.revisions)

    add_repos_to_triplestore(repos, init)
    return "<h1>Repo harvester updated!</h1>"
