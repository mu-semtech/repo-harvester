"""Defines the GitHub Reposource subclass. All GitHub API code should be contained in this file."""

# Built-in imports
from typing import List, Dict

# Relative imports
from ..config import categories_from_conf
from ..utils import log, json
from ..reposource import Reposource
from ..imagesource import Imagesource
from ..Category import Category
from ..Repo import Repo


class GitHub(Reposource):
    def __init__(self, owner: str, imagesource: Imagesource) -> None:
        super().__init__(imagesource)
        self.owner = owner
        self.repos: List[Repo] = []
    
    def _parse_category_from_data(self, repo_other_data: object, categories:Dict[str, Category]=categories_from_conf) -> Category:
        """Override implementation: see Reposource for more info"""
        if repo_other_data["archived"]:
            return categories["archive"]
        else:
            return None
        
    def repo_from_api(self, repo_json, categories: Dict[str, Category]=categories_from_conf):
        """From a GitHub API object, create a Repo object and add it to to self.repos"""
        repo = Repo(
            name=repo_json["name"],
            description=repo_json["description"],
            repo_url=repo_json["html_url"],
            homepage_url=repo_json["homepage"],
            reposource=self,
            category_data=repo_json,
            other_data=repo_json,
            categories=categories
        )
      
        return repo
        #self.repos.append(repo)

    def get_all_repo_data(self) -> list:
        """ Requests all the repos of the specified user/organisation from GitHub's API, returning the parsed json response"""
        page_size = 100
        result_count = page_size
        page = 1
        all_repos = []
        # If this is true, the max amount got returned, thus there is possible more in the next page
        while result_count == page_size:
            data = json(f"https://api.github.com/orgs/{self.owner}/repos?per_page={page_size}&page={page}")
            result_count = len(data)

            if result_count > 0:
                all_repos += data
            page += 1


        return all_repos

    def url_generator(self, repo: Repo, version: str=None):
        """Override implementation: see Reposource for more info"""
        if version == None:
            version = repo.other_data["default_branch"]
        return "https://github.com/{0}/tree/{1}".format(
            repo.other_data["full_name"], version
        )

    def load_repos(self, categories: Dict[str, Category]=categories_from_conf):
        """Override implementation: see Reposource for more info"""
        repos_data = self.get_all_repo_data()
        for repo_data in repos_data:
            self.repos.append(self.repo_from_api(repo_data, categories))
