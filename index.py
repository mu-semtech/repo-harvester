from reposource.github import GitHub
from imagesource.dockerhub import DockerHub
from categories import categories

if __name__ == "__main__":
    """Get the repos, parse them, sort them by category, export them to build/*.html"""
    #repos = list_and_parse_repos()
    mu_semtech_github = GitHub(owner="mu-semtech", imagesource=DockerHub(owner="semtech"))

    dict_category_repos = {}
    for category_id in categories:
        if category_id == categories["archive"].id:
            print("Skipping archive!")
            continue
        
        category = categories[category_id]
        category_repos = [repo for repo in mu_semtech_github.repos if repo.category.id == category_id]

        dict_category_repos[category.name] = category_repos
    
    print(dict_category_repos)

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
