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



def import_resources_prefixes(path) -> List[Prefix]:
    with open(path, mode="r", encoding="UTF-8") as file:
        data = file.read()
    
    re_prefixes = r'^(\(add-prefix )"(\S*)" "(\S*)"(\))'

    matches = findall(re_prefixes, data, IGNORECASE | MULTILINE)
    prefixes = []
    for match in matches:
        prefixes.append(Prefix(match[1], match[2]))

    return prefixes

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
    prefixes = import_resources_prefixes("config/resources/repository.lisp")
    
    prefixes.append(Prefix("mu", "http://mu.semte.ch/vocabularies/core/"))

    sparql = setup_sparql()

    query = ""

    for prefix in prefixes:
        query += prefix.to_sparql_syntax() + "\n"
    
    query += "\nINSERT DATA {\n"
    
    for repo in repos:

        format_string = QUERY_WITH_IMAGE if repo.image.url != "" else QUERY_NO_IMAGE

        
        print("----------")
        print(escape(repo.readme))
        query += format_string.format(
                uuid=uuid3(NAMESPACE_DNS, repo.name),
                title=repo.name,
                description=repo.description,
                category=repo.category.url,
                
                readme=
                   # escape(Markup(
                        repo.readme
                        .replace("\\", "&bsol;")
                        .replace('"', "&quot;")
                        #.replace("'", "&apos;")
                        .replace("\n", "\\n")
                        #.replace("*", "")   
                    #))
                    ,

                repoUrl=repo.repo_url,
                imageUrl=repo.image.url
            )
    
    query += "}\n"

    #print(query)
    run_sparql(sparql, query)

    

