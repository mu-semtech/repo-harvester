from typing import List
from helpers import generate_uuid, update, log
from escape_helpers import sparql_escape_string, sparql_escape_time, sparql_escape_uri
from datetime import datetime
from Repo import Repo
from uuid import uuid3, NAMESPACE_DNS
from re import search, IGNORECASE, MULTILINE

PREFIXES = """
  PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
  PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
  PREFIX dct: <http://purl.org/dc/terms/>
"""

# TODO fix DRY
SPARQL_REPO_BASE = """
GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo;
    mu:uuid {uuid};
    dct:title {title};
    dct:description {description};
    ext:category {category}EXTRA.
}}
"""

SPARQL_REPO_NO_IMAGE = SPARQL_REPO_BASE.replace("EXTRA", "")
SPARQL_REPO_WITH_IMAGE = SPARQL_REPO_BASE.replace("EXTRA", ";\next:    ext:imageUrl {imageUrl}.")

SPARQL_DELETE_INSERT = """
DELETE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo; dct:title ?title; dct:description ?description; ext:category ?category.
  }}
}} INSERT {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo;
    mu:uuid {uuid};
    dct:title {title};
    dct:description {description};
    ext:category {category}EXTRA.
  }}
}} WHERE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo.
    OPTIONAL {{ {resource} dct:title ?title }}
    OPTIONAL {{ {resource} dct:description ?description }}
    OPTIONAL {{ {resource} ext:category ?category }}
  }}
}}
"""

def replace_to_insert(regex_string):
  regex = search(r"INSERT(.|\n)*(?=WHERE(\s|{))", regex_string, MULTILINE)
  insert = PREFIXES + regex.group(0)
  return insert



SPARQL_REVISION = """
DELETE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:RepoRevision; ext:revisionImageTag ?imageTag; ext:revisionImageUrl ?imageUrl; ext:revisionRepoTag ?repoTag; ext:revisionRepoUrl ?repoUrl; ext:readme ?readme; ext:hasRepo ?hasRepo.
  }}
}} INSERT {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:RepoRevision;
    mu:uuid {uuid};

    ext:revisionImageTag {imagetag};
    ext:revisionImageUrl {imageurl};

    ext:revisionRepoTag {repotag};
    ext:revisionRepoUrl {repourl};
    
    ext:readme {readme};
    
    ext:hasRepo {repograph}.
  }}
}} WHERE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:RepoRevision;
    ext:hasRepo {repograph}.
  }}
}}
"""

def clear_all_triples():
    log("Refusing to delete all triples")
    # Don't, this is not only your data you will be destroying
    # query('DROP SILENT GRAPH <http://mu.semte.ch/application>')


def add_repos_to_triplestore(repos: List[Repo], init=False):

    
    #query_string_repos += "\nINSERT DATA {\n"

    
    for repo in repos:
        query_string_repos = ""

        query_string_repos += PREFIXES
        query_string_repos += "\n"



        #format_string = SPARQL_REPO_WITH_IMAGE if repo.image.url != "" else SPARQL_REPO_NO_IMAGE
        repo_uuid = str(uuid3(NAMESPACE_DNS, repo.name)) #generate_uuid()
        query_string_repos += SPARQL_DELETE_INSERT.replace("EXTRA", ";\n    ext:imageUrl {imageUrl}" if repo.image.url != "" else "").format(
            resource=f"<http://info.mu.semte.ch/repos/{repo_uuid}>",
            uuid=sparql_escape_string(repo_uuid),
            title=sparql_escape_string(repo.name), # + datetime.today().strftime("-%H-%M-%S"),
            description=sparql_escape_string(repo.description),
            category=sparql_escape_uri(repo.category.url),
            #readme=
            imageUrl=sparql_escape_uri(repo.image.url)
        )

        if init:
          print("REIGU")
          query_string_repos = replace_to_insert(query_string_repos)
          print(query_string_repos)


        #print(query_string_repos)
        update(query_string_repos)
        
        for revision in repo.revisions:
          query_string_revisions = PREFIXES + "\n"

          print(revision)

          revision_uuid = generate_uuid()
          query_string_revisions += SPARQL_REVISION.format(
              resource=f"<http://info.mu.semte.ch/repo-revisions/{revision_uuid}>",
              uuid=sparql_escape_string(revision_uuid),
              imagetag = sparql_escape_string(revision.image_tag or "None"),
              imageurl = sparql_escape_uri(revision.image_url or "None"),
              repotag = sparql_escape_string(revision.repo_tag or "None"),
              repourl = sparql_escape_uri(revision.repo_url or "None"),
              
              repograph = sparql_escape_uri(f"http://info.mu.semte.ch/repos/{repo_uuid}"),


              
              readme = sparql_escape_string(revision.readme)
              #         .replace("\\", "&bsol;")
              #         .replace('"', "&quot;")
              #         .replace("\n", "\\n")
              
          )

          if init:
            query_string_revisions = replace_to_insert(query_string_revisions)

          update(query_string_revisions)

    
    #for query_string in [query_string_repos, query_string_revisions]:
     #   query_string += "}\n"
      #  log(query_string)
       # update(query_string)

    #print(query)
    #run_sparql(sparql, query_string)

    

