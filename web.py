from src.repo_harvester import load_repos_from_config
from src.repo_harvester.sparql import add_repos_to_triplestore 

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
    
    repos = load_repos_from_config()

    add_repos_to_triplestore(repos, init)
    return "<h1>Repo harvester updated!</h1>"
