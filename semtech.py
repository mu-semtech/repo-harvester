from typing import List
from re import findall, IGNORECASE, MULTILINE
from Repo import Repo
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST

class Prefix():
    def __init__(self, key, url) -> None:
        self.key = key
        self.url = url
    
    def to_sparql_syntax(self):
        return f"PREFIX {self.key}: <{self.url}>"
    
    def __str__(self) -> str:
        return self.to_sparql_syntax()
    
    def __repr__(self) -> str:
        return self.to_sparql_syntax()



def import_resources_prefixes(path) -> List[Prefix]:
    print("meow")
    with open(path, mode="r", encoding="UTF-8") as file:
        data = file.read()
    
    re_prefixes = r'^(\(add-prefix )"(\S*)" "(\S*)"(\))'

    matches = findall(re_prefixes, data, IGNORECASE | MULTILINE)
    prefixes = []
    for match in matches:
        prefixes.append(Prefix(match[1], match[2]))

    return prefixes


def add_repos_to_triplestore(repos: List[Repo]):
    prefixes = import_resources_prefixes("config/resources/repository.lisp")
    

    sparql = SPARQLWrapper("localhost:8890")
    sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("dba", "dba")
    sparql.setMethod("POST")

    query = ""

    for prefix in prefixes:
        query += prefix.to_sparql_syntax() + "\n"

    
    

    print(query)

    return

    sparql.setQuery(query)
    pass

