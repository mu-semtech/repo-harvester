from reposource.GitHub import GitHub
from imagesource.DockerHub import DockerHub
from categories import sort_into_category_dict
from sparql import add_repos_to_triplestore, clear_all_triples
from helpers import log

@app.route("/")
def index():
    return "Repo harvester online!"

@app.route("/init", methods=["GET", "POST"])
def init():
    return add_repos(init=True)


@app.route("/update", methods=["GET", "POST"])
def update():
    return add_repos(init=False)


def add_repos(init=False):
    log("Updating...")
    """Get the repos, parse them, sort them by category, export them to build/*.html"""
    repos = []
    mu_semtech_github = GitHub(owner="mu-semtech", imagesource=DockerHub(owner="semtech"))
    repos += mu_semtech_github.repos

    dict_category_repos = sort_into_category_dict(mu_semtech_github.repos)

    log(dict_category_repos)

    repo = mu_semtech_github.repos[8]
    log(repo)
    log(repo.description)
    log(repo.image)
    log(repo.revisions)


    add_repos_to_triplestore(repos, init)
    return "<h1>Repo harvester updated!</h1>"
