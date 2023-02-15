from typing import List
from re import findall, IGNORECASE, MULTILINE, sub
from Repo import Repo
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, BASIC
from urllib.error import HTTPError
from uuid import uuid3, NAMESPACE_DNS
from markupsafe import Markup, escape
from datetime import datetime
from helpers import generate_uuid, query, update
from escape_helpers import sparql_escape

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

    ext:repositoryUrl "{repoUrl}";
    ext:imageUrl "{imageUrl}".
}}
"""

REVISION = """
GRAPH <http://mu.semte.ch/application> {{
    <http://info.mu.semte.ch/repo-revisions/{uuid}> a ext:RepoRevision;
    mu:uuid "{uuid}";

    ext:revisionImageTag "{imagetag}";
    ext:revisionImageUrl "{imageurl}";

    ext:revisionRepoTag "{repotag}";
    ext:revisionRepoUrl "{repourl}";
    
    ext:hasRepo "{repograph}".

}}
"""

def clear_all_triples():
    query('DROP SILENT GRAPH <http://mu.semte.ch/application>')


def add_repos_to_triplestore(repos: List[Repo]):
    query_string_repos = ""

    for prefix in PREFIXES:
        query_string_repos += prefix.to_sparql_syntax() + "\n"
    
    query_string_repos += "\nINSERT DATA {\n"

    query_string_revisions = query_string_repos
    
    for repo in repos:

        format_string = QUERY_WITH_IMAGE if repo.image.url != "" else QUERY_NO_IMAGE

        repo_uuid = generate_uuid()
        
        query_string_repos += format_string.format(
                uuid=repo_uuid,
                title=repo.name + datetime.today().strftime("-%H-%M-%S"),
                description=repo.description,
                category=repo.category.url,
                
                #readme=

                repoUrl=repo.repo_url,
                imageUrl=repo.image.url
            )
        
        for revision in repo.revisions:
            query_string_revisions += REVISION.format(
                uuid=generate_uuid(),

                imagetag = sparql_escape(revision.image_tag),
                imageurl = sparql_escape(revision.image_url),

                repograph = sparql_escape(f"<http://info.mu.semte.ch/repos/{repo_uuid}>"),

                repotag = sparql_escape(revision.repo_tag),
                repourl = sparql_escape(revision.repo_url),

                
                # readme = sparql_escape(revision.readme)
                #         .replace("\\", "&bsol;")
                #         .replace('"', "&quot;")
                #         .replace("\n", "\\n")
                
            )

    
    for query_string in [query_string_repos, query_string_revisions]:

        query_string += "}\n"
        query(query_string)

    #print(query)
    #run_sparql(sparql, query_string)

    

