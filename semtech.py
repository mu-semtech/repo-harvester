from typing import List
from re import findall, IGNORECASE, MULTILINE, sub
from Repo import Repo
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, BASIC
from urllib.error import HTTPError
from uuid import uuid3, NAMESPACE_DNS
from markupsafe import Markup, escape

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

PREFIXES = [
    Prefix("mu", "http://mu.semte.ch/vocabularies/core/"),
    Prefix("ext", "http://mu.semte.ch/vocabularies/ext/"),
    Prefix("dct", "http://purl.org/dc/terms/")
]

# TODO fix DRY
QUERY_NO_IMAGE = """
GRAPH <http://mu.semte.ch/application> {{
    <http://info.mu.semte.ch/repos/{uuid}> a ext:Repo;
    mu:uuid "{uuid}";
    dct:title "{title}";
    dct:description "{description}";
    ext:category "{category}";
    ext:readme "{readme}";

    ext:repositoryUrl "{repoUrl}".
}}
"""

QUERY_WITH_IMAGE = """
GRAPH <http://mu.semte.ch/application> {{
    <http://info.mu.semte.ch/repos/{uuid}> a ext:Repo;
    mu:uuid "{uuid}";
    dct:title "{title}";
    dct:description "{description}";
    ext:category "{category}";
    ext:readme "{readme}";

    ext:repositoryUrl "{repoUrl}";
    ext:imageUrl "{imageUrl}".
}}
"""

REVISION = """
GRAPH <http://mu.semte.ch/application> {{
    <http://info.mu.semte.ch/repos/{uuid}> a ext:RepoRevision;
    mu:uuid "{uuid}";
    ext:revisionImageTag "{title}";
    dct:description "{description}";
    ext:category "{category}";
    ext:readme "{readme}";

    ext:repositoryUrl "{repoUrl}";
    ext:imageUrl "{imageUrl}".
}}
"""

def setup_sparql():
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setHTTPAuth(BASIC)
    sparql.setCredentials("dba", "dba")
    sparql.setMethod("POST")
    
    sparql.addDefaultGraph("http://info.mu.semte.ch/repos/")
    return sparql

def run_sparql(sparql, query):
    sparql.setQuery(query)
    try:
        exec = sparql.query()
        print(exec.info())
        #print (exec.info())
    except HTTPError as e:
        print(e)

def clear_all_triples():
    sparql = setup_sparql()
    run_sparql(sparql, 'DROP SILENT GRAPH <http://mu.semte.ch/application>')


def add_repos_to_triplestore(repos: List[Repo]):
    sparql = setup_sparql()

    query = ""

    for prefix in PREFIXES:
        query += prefix.to_sparql_syntax() + "\n"
    
    query += "\nINSERT DATA {\n"
    
    for repo in repos:

        format_string = QUERY_WITH_IMAGE if repo.image.url != "" else QUERY_NO_IMAGE

        
        query += format_string.format(
                uuid=uuid3(NAMESPACE_DNS, repo.name),
                title=repo.name,
                description=repo.description,
                category=repo.category.url,
                
                #readme=

                repoUrl=repo.repo_url,
                imageUrl=repo.image.url
            )
        
    query += "}\n"

    #print(query)
    run_sparql(sparql, query)

    

