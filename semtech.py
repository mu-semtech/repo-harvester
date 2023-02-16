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
QUERY_NO_IMAGE = """
GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo;
    mu:uuid {uuid};
    dct:title {title};
    dct:description {description};
    ext:category {category}.
}}
"""

QUERY_WITH_IMAGE = """
GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:Repo;
    mu:uuid {uuid};
    dct:title {title};
    dct:description {description};
    ext:category {category};
    ext:imageUrl {imageUrl}.
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
    log("Refusing to delete all triples")
    # Don't, this is not only your data you will be destroying
    # query('DROP SILENT GRAPH <http://mu.semte.ch/application>')


def add_repos_to_triplestore(repos: List[Repo]):
    query_string_repos = ""

    query_string_repos += PREFIXES
    query_string_repos += "\n"
    
    query_string_repos += "\nINSERT DATA {\n"

    query_string_revisions = query_string_repos
    
    for repo in repos:
        format_string = QUERY_WITH_IMAGE if repo.image.url != "" else QUERY_NO_IMAGE
        repo_uuid = generate_uuid()
        query_string_repos += format_string.format(
            resource=sparql_escape_uri(repo.repo_url),
            uuid=sparql_escape_string(repo_uuid),
            title=sparql_escape_string(repo.name), # + datetime.today().strftime("-%H-%M-%S"),
            description=sparql_escape_string(repo.description),
            category=sparql_escape_uri(repo.category.url),
            #readme=
            imageUrl=sparql_escape_uri(repo.image.url)
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
        log(query_string)
        update(query_string)

    #print(query)
    #run_sparql(sparql, query_string)

    

