from src.repo_harvester import load_repos_from_config, log
from src.repo_harvester.linkeddata import add_repos_to_triplestore 
from src.microservice import stream_progress, stream_template
from src.microservice.flask import get_template
from flask import stream_with_context, copy_current_request_context, Response, make_response, redirect
import src.repo_harvester.globals
from threading import Thread

"""
Entrypoint for the repo-harvester:
- Defines endpoints
- Defines repo & image sources

app should not be defined here, as this is handled by mu-python-template
"""

template = get_template()


@app.route("/")
def index():
    """Simple status page to check if the repo harvester works"""
    return get_template()

@app.route("/init", methods=["GET", "POST"])
def init():
    """Calls add_repos_to_triplestore with init, initialising the database"""
    return add_repos(init=True)


@app.route("/update", methods=["GET", "POST"])
def update():
    """Calls add_repos_to_triplestore without init, updating the database"""
    return add_repos(init=False)

def add_repos(init=False):
    repos = load_repos_from_config()

    add_repos_to_triplestore(repos, init)
    return "<h1>Updated</h1>"

@app.route("/listen", methods=["GET", "POST"])
def listen():
    """Calls add_repos_to_triplestore without init, updating the database"""
    def generator():
        import time
        while True:
            time.sleep(1)
            yield src.repo_harvester.globals.response
            src.repo_harvester.globals.response = ""

    
    return Response(stream_with_context(generator()), content_type="text/event-stream")
    #return src.repo_harvester.globals.response

