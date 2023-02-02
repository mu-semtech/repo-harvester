from typing import List
from Repo import Repo
from reposource.Reposource import Reposource
from imagesource.Imagesource import Imagesource
from categories import Category, categories
from request import json

class GitHub(Reposource):
    """
    The GitHub :class:`Reposource`
    """
    def __init__(self, owner: str, imagesource: Imagesource) -> None:
        super().__init__(imagesource)
        self.owner = owner
        self.repos: List[Repo] = []

        repos_data = self.get_all_repos()
        for repo_data in repos_data:
            self.add_repo(repo_data)
        
        
    
    # def get_revisions(self):
    #     for repo in self.repos:
    #         docker_tags = repo
    #         for tag in tags:
    #             tag.name

    #         print("Sleeping to prevent rate limiting...")
    #         sleep(5)
        
    
    
    def add_repo(self, repo_json):

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
        for tag_object in tag_array:
            repo.tags.append(tag_object["name"])
            #repo.tags.append(Tag(tag_object["name"], tag_object["commit"]))
      
        self.repos.append(repo)
    
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
        request = json("https://api.github.com/orgs/{}/repos".format(self.owner))
        return request




    def file_url_generator(repo: Repo, filename: str) -> str:
        return "https://raw.githubusercontent.com/{0}/{1}/{2}".format(
                repo.other_data.full_name, repo.other_data.default_branch, filename)
