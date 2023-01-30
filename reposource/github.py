from requests import get
from typing import List
from Repo import Repo, Reposource, Category, categories

class GitHub(Reposource):
    """
    The GitHub :class:`Reposource`
    """
    def __init__(self, owner: str) -> None:
        super().__init__()
        self.owner = owner

        repos_data = self.get_all_repos()
        self.repos = self.repo_class_list_from_json(repos_data)
    
    
    def _parse_category(self, repo_other_data) -> Category:
        """Code to determine the Category from GitHub data"""
        if repo_other_data["archived"]:
            return categories["archive"]
        else:
            return None


    def get_all_repos(self) -> object:
        """ Simply requests all the repos of the specified user/organisation from GitHub API,
        returning the parsed json response
        """
        request = get("https://api.github.com/orgs/{}/repos".format(self.owner))
        return request.json()


    def repo_class_list_from_json(self, json) -> List[Repo]:
        """ 
        When given , but returns repos parsed into the Repo class
        """
        parsed_repos = []
        for repo_data in json:
            parsed_repos.append(Repo(
                name=repo_data["name"],
                reposource=self,
                category_data=repo_data,
                other_data=repo_data
                ))
        return parsed_repos


    def file_url_generator(repo: Repo, filename: str) -> str:
        return "https://raw.githubusercontent.com/{0}/{1}/{2}".format(
                repo.other_data.full_name, repo.other_data.default_branch, filename)
