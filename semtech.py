from typing import List
from helpers import generate_uuid, update, log
from escape_helpers import sparql_escape_string, sparql_escape_time, sparql_escape_uri
from datetime import datetime
from Repo import Repo

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
    {{resource}} a ext:Repo; dct:title ?title; dct:description ?description; ext:category ?category.
  }}
}} INSERT {{
  GRAPH <http://mu.semte.ch/application> {{
    {{resource}} a ext:Repo;
    mu:uuid {uuid};
    dct:title {title};
    dct:description {description};
    ext:category {category}EXTRA.
}}
}} WHERE {{
  GRAPH <http://mu.semte.ch/application> {{
    {{resource}} a ext:Repo.
    OPTIONAL {{ {{resource}} dct:title ?title }}
    OPTIONAL {{ {{resource}} dct:description ?description }}
    OPTIONAL {{ {{resource}} ext:category ?category }}
  }}
}}
"""



SPARQL_REVISION = """
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
    log("Refusing to delete all triples")
    # Don't, this is not only your data you will be destroying
    # query('DROP SILENT GRAPH <http://mu.semte.ch/application>')


def add_repos_to_triplestore(repos: List[Repo]):

    
    #query_string_repos += "\nINSERT DATA {\n"

    
    for repo in repos:
        query_string_repos = ""

        query_string_repos += PREFIXES
        query_string_repos += "\n"

        query_string_revisions = query_string_repos


        #format_string = SPARQL_REPO_WITH_IMAGE if repo.image.url != "" else SPARQL_REPO_NO_IMAGE
        repo_uuid = generate_uuid()
        query_string_repos += SPARQL_DELETE_INSERT.replace("EXTRA", ";\n    ext:imageUrl {imageUrl}" if repo.image.url != "" else "").format(
            resource=sparql_escape_uri(repo.repo_url),
            uuid=sparql_escape_string(repo_uuid),
            title=sparql_escape_string(repo.name), # + datetime.today().strftime("-%H-%M-%S"),
            description=sparql_escape_string(repo.description),
            category=sparql_escape_uri(repo.category.url),
            #readme=
            imageUrl=sparql_escape_uri(repo.image.url)
        )
        update(query_string_repos)
        
        for revision in repo.revisions:
            continue
            query_string_revisions += SPARQL_REVISION.format(
                uuid=generate_uuid(),

                imagetag = sparql_escape_string(revision.image_tag),
                imageurl = sparql_escape_uri(revision.image_url),

                repograph = sparql_escape_uri(f"<http://info.mu.semte.ch/repos/{repo_uuid}>"),

                repotag = sparql_escape_string(revision.repo_tag),
                repourl = sparql_escape_string(revision.repo_url),

                
                # readme = sparql_escape(revision.readme)
                #         .replace("\\", "&bsol;")
                #         .replace('"', "&quot;")
                #         .replace("\n", "\\n")
                
            )
            update(query_string_revisions)

    
    #for query_string in [query_string_repos, query_string_revisions]:
     #   query_string += "}\n"
      #  log(query_string)
       # update(query_string)

    #print(query)
    #run_sparql(sparql, query_string)

    

