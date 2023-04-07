# Native imports
from time import perf_counter, sleep
# Relative imports
from reposource.GitHub import GitHub
from imagesource.DockerHub import DockerHub
from categories import sort_into_category_dict
from sparql import add_repos_to_triplestore
# Package imports
from helpers import log
from info import info, response
from flask import stream_with_context, Response

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

    start_time = perf_counter()
    info("Adding repos to the database...")
    info(f"Running add_repos. init: {init}...")
    
    repos = []

    mu_semtech_github = GitHub(owner="mu-semtech", imagesource=DockerHub(owner="semtech"))
    repos += mu_semtech_github.repos
    info("mu_semtech github added to repos")

    add_repos_to_triplestore(repos, init)

    time_elapsed = perf_counter() - start_time
    info(f"Done! time_elapsed: {time_elapsed}s")
    
    info(f"<h1>Repo harvester updated!</h1>")

    return response()

    
