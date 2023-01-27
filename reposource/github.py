from requests import get
from typing import List
from .Reposource import Reposource, Repo

"""I tried to contain all GitHub specific-code here,
in an attempt to make sure the other code is as platform-agnostic as possible
"""

class GitHub(Reposource):
    def __init__(self, owner: str) -> None:
        self.owner = owner
        super().__init__(self.list_and_parse_repos())


    def list_repos_json(self):
        """ Simply requests all the repos of the specified user/organisation from GitHub API,
        returning the parsed json response
        """
        request = get("https://api.github.com/orgs/{}/repos".format(self.owner))
        return request.json()


    def list_and_parse_repos(self) -> List[Repo]:
        """ Leverages list_repos, but returns repos parsed into the Repo class
        """
        unparsed_repos = self.list_repos_json()
        parsed_repos = []
        for repo in unparsed_repos:
            parsed_repos.append(Repo(repo))
        return parsed_repos


    def file_url_generator(object, filename):
        return "https://raw.githubusercontent.com/{0}/{1}/{2}".format(
                object.full_name, object.default_branch, filename)

    @staticmethod
    def parse_category(repo):
        """An appendix to Repo.parse_category, but with Github specific api stuff"""
        if repo["archived"]:
            return "archive"
        else:
            return None
        """
        Unused, as mu-project is a template but part of core
        if repo["is_template"]:
            return category["templates"]
        """