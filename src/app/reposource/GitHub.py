# Native imports
from typing import List, Dict
# Relative imports
from ..utils.request import json
from ..Repo import Repo
from .Reposource import Reposource
from ..imagesource.Imagesource import Imagesource
from ..Category import Category
from ..utils.categories import categories
# Package imports
try:
    from helpers import log
except ModuleNotFoundError:
    log = print

"""Defines the GitHub Reposource subclass. All GitHub API code should be contained in this file."""

class GitHub(Reposource):
    def __init__(self, owner: str, imagesource: Imagesource) -> None:
        super().__init__(imagesource)
        self.owner = owner
        self.repos: List[Repo] = []
    
    def _parse_category_from_data(self, repo_other_data: object, categories:Dict[str, Category]=categories) -> Category:
        """Override implementation: see Reposource for more info"""
        if repo_other_data["archived"]:
            return categories["archive"]
        else:
            return None
        
    def repo_from_api(self, repo_json):
        """From a GitHub API object, create a Repo object and add it to to self.repos"""
        repo = Repo(
            name=repo_json["name"],
            description=repo_json["description"],
            repo_url=repo_json["html_url"],
            homepage_url=repo_json["homepage"],
            reposource=self,
            category_data=repo_json,
            other_data=repo_json
        )

        print(f"Fetching tags for {repo.name}")
        tag_array = json(f"https://api.github.com/repos/{self.owner}/{repo.name}/tags", 5)
        if type(tag_array) is not list:
            tag_array = tag_array.results

        for tag_object in tag_array:
            repo.tags.append(tag_object["name"])
            #repo.tags.append(Tag(tag_object["name"], tag_object["commit"]))
      
        return repo
        #self.repos.append(repo)

    def get_all_repos(self) -> object:
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

    def file_url_generator(self, repo: Repo, filename: str, version: str=None) -> str:
        """Override implementation: see Reposource for more info"""
        if version == None:
            version = repo.other_data["default_branch"]
        return "https://raw.githubusercontent.com/{0}/{1}/{2}".format(
                repo.other_data["full_name"], version, filename)
