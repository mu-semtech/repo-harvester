from reposource.github import GitHub
from imagesource.dockerhub import DockerHub
from categories import categories, sort_into_category_dict

if __name__ == "__main__":
    """Get the repos, parse them, sort them by category, export them to build/*.html"""
    #repos = list_and_parse_repos()
    mu_semtech_github = GitHub(owner="mu-semtech", imagesource=DockerHub(owner="semtech"))

    dict_category_repos = sort_into_category_dict(mu_semtech_github.repos)

    print(mu_semtech_github.repos[0].image)
    # api = Api.config({
    #     "API_ROOT": "http://localhost/"
    # })

    # endpoint = api.endpoint('microservices')
    
    # for repo in mu_semtech_github.repos:
        
    #     endpoint.put(object=JsonApiObject(
    #         type="microservices",
    #         attributes = {
    #             "title": "meowmeows"
                
    #         }
    #     ))
