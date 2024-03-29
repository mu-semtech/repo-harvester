# Built-in imports
from time import sleep
import threading

# Relative imports
from src.repo_harvester import load_repos_from_config, log
from src.repo_harvester.linkeddata import add_repos_to_triplestore 
from src.microservice import get_template
import src.microservice

# Package imports
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
    return get_template()

@app.route("/update", methods=["GET", "POST"])
def update():
    """Calls add_repos_to_triplestore with init, initialising the database"""
    src.microservice.listening = True
    thread = threading.Thread(target=run)
    thread.start()
    
    return "Init..."
    return add_repos(init=True)

def run():
    repos = load_repos_from_config()
    add_repos_to_triplestore(repos, True)
    add_repos_to_triplestore(repos, False)
    src.microservice.listening = False

def add_repos(init=False):
    src.microservice.listening = True
    repos = load_repos_from_config()



    thread = threading.Thread(target=run, args=(repos, init,))
    thread.start()

    
    return "Updating..."

@app.route("/listen", methods=["GET", "POST"])
def listen():
    """Calls add_repos_to_triplestore without init, updating the database"""
    def generator():
        sleep(2)  # Give the request some time
        while src.microservice.listening:
            sleep(0.5)
            yield src.microservice.send_to_html
            src.microservice.send_to_html = ""

    
    return Response(stream_with_context(generator()), content_type="text/event-stream")

