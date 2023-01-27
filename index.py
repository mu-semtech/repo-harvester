from github import list_and_parse_repos
from Repo import categories

if __name__ == "__main__":
    """Get the repos, parse them, sort them by category, export them to build/*.html"""
    repos = list_and_parse_repos()

    dict_category_repos = {}
    for category_id in categories:
        if category_id == categories["archive"].id:
            print("Skipping archive!")
            continue
        
        category = categories[category_id]
        category_repos = [repo for repo in repos if repo.category.id == category_id]

        dict_category_repos[category.name] = category_repos
    
    print(dict_category_repos)
