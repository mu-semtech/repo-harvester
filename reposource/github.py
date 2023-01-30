from requests import get
from typing import List
from Repo import Repo, Reposource, categories

class GitHub(Reposource):
    """
    The GitHub :class:`Reposource`
    """
    def __init__(self, owner: str) -> None:
        super().__init__()
        self.owner = owner

        repos_data = self.get_all_repos()
        self.repos = self.list_and_parse_repos(repos_data)
    
    
    def _parse_category(self, data):
        """Code to determine the Category from GitHub data"""
        if data["archived"]:
            return categories["archive"]
        else:
            return None


    def get_all_repos(self):
        """ Simply requests all the repos of the specified user/organisation from GitHub API,
        returning the parsed json response
        """
        request = get("https://api.github.com/orgs/{}/repos".format(self.owner))
        return request.json()


    def list_and_parse_repos(self, repos_data) -> List[Repo]:
        """ 
        When given , but returns repos parsed into the Repo class
        """
        parsed_repos = []
        for repo_data in repos_data:
            parsed_repos.append(Repo(
                name=repo_data["name"],
                reposource=self,
                category_data=repo_data,
                other_data=repo_data
                ))
        return parsed_repos


    def file_url_generator(repo: Repo, filename: str):
        return "https://raw.githubusercontent.com/{0}/{1}/{2}".format(
                repo.other_data.full_name, repo.other_data.default_branch, filename)
