from Repo import Repo
from abc import abstractmethod
from typing import List

class Reposource():
    def __init__(self, repos: List[Repo]) -> None:
        self.repos = repos
    
    def parse_category(self):
        """When given a repo json, determine the category"""
        api_parseable = reposource.parse_category(json)
        if api_parseable != None:
            return categories[api_parseable]

        else:
            for override in overrides:
                if search(override, json["name"], IGNORECASE):
                    return overrides[override]
                    
            return _parse_category_from_name(json["name"])
