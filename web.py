from reposource.github import GitHub
from imagesource.dockerhub import DockerHub
from categories import categories, sort_into_category_dict
from semtech import add_repos_to_triplestore, clear_all_triples



@app.route("/")
def index():
    print("index")
    return "<h1>Repo harvester online!</h1>"


@app.route("/update", methods=["GET", "POST"])
def update():
    print("Updating...")
    """Get the repos, parse them, sort them by category, export them to build/*.html"""
    #repos = list_and_parse_repos()
    mu_semtech_github = GitHub(owner="mu-semtech", imagesource=DockerHub(owner="semtech"))

    dict_category_repos = sort_into_category_dict(mu_semtech_github.repos)

    print(dict_category_repos)

    repo = mu_semtech_github.repos[8]
    print(repo)
    print(repo.description)
    print(repo.image)
    print(repo.revisions)

    clear_all_triples()

    add_repos_to_triplestore(mu_semtech_github.repos)
    return "<h1>Repo harvester updated!</h1>"
