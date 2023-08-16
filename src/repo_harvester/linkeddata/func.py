# Built-in imports
from re import search, MULTILINE
from typing import List
from uuid import uuid3, NAMESPACE_DNS
# Relative imports
from ..Repo import Repo
from ..utils import log
from .prefixes import PREFIXES
from .sparql_format_strings import SPARQL_STRING_REPO, SPARQL_STRING_REVISION

# mu-python-template imports
try:
  from helpers import generate_uuid, update
  from escape_helpers import sparql_escape_string, sparql_escape_time, sparql_escape_uri
except ModuleNotFoundError:
   def update(): return None
   def sparql_escape_string(): return None
   def sparql_escape_uri(): return None
  


"""
All the SPARQL/database relevant code.
- Defines PREFIXES & SPARQL query format strings
- Populates the triplestore using the above definitions
"""




def replace_to_insert(regex_string, prefixes=PREFIXES):
  """Removes the DELETE & WHERE from a SPARQL query string, only leaving INSERT"""
  regex = search(r"INSERT(.|\n)*(?=WHERE(\s|{))", regex_string, MULTILINE)
  insert = prefixes + regex.group(0)
  return insert

def add_repos_to_triplestore(repos: List[Repo], init=False,  prefixes=PREFIXES, sparql_string_repo=SPARQL_STRING_REPO, sparql_string_revision=SPARQL_STRING_REVISION):
    """When given a List of Repo objects, initialise/update the triplestore"""    
    #yield "Meow"
    for repo in repos:
        log("INFO", "Adding "  + repo.name)
        #yield repo.name
        #yield "Adding " + repo.name
        repo_uuid = str(uuid3(NAMESPACE_DNS, repo.name)) #generate_uuid()
      

        query_string_repos = prefixes
        query_string_repos += "\n"

        extra_args = ""
        #extra_args += ";\n    ext:imageUrl {imageUrl}" if repo.image != None else ""

        image_url = repo.image.url if repo.image else ""

        query_string_repos += sparql_string_repo.replace("EXTRA", extra_args).format(
            resource=f"repos:{repo_uuid}",
            uuid=sparql_escape_string(repo_uuid),
            title=sparql_escape_string(repo.name), # + datetime.today().strftime("-%H-%M-%S"),
            description=sparql_escape_string(repo.description),
            category=sparql_escape_uri(repo.category.url),
            #imageUrl=sparql_escape_uri(image_url) 
        )

        if init:
          query_string_repos = replace_to_insert(query_string_repos)
        
        log("INFO", "Updating repo..." + repo.name)
        #yield "Updating " + repo.name
        #with app.app_context():
        update(query_string_repos)
        log("INFO", "Updated repo " + repo.name)
        
        for revision in repo.revisions():
          log("INFO", revision.repo_tag)
          #yield "<li>Importing revision" +  str(revision.repo_tag)+ "</li>"
          query_string_revisions = prefixes + "\n"
          

          revision_uuid = str(uuid3(NAMESPACE_DNS, f"{repo.name}-{revision.repo_tag}"))
          revision_resource = f"revisions:{revision_uuid}"


          query_string_revisions += sparql_string_revision.format(
              resource=revision_resource,
              uuid=sparql_escape_string(revision_uuid),
              imagetag = sparql_escape_string(revision.image_tag or "None"),
              imageurl = sparql_escape_uri(revision.image_url or "None"),
              repotag = sparql_escape_string(revision.repo_tag or "None"),
              repourl = sparql_escape_uri(revision.repo_url or "None"),
              
              repograph = f"repos:{repo_uuid}",
              
              readme = sparql_escape_string(revision.readme),
              tutorials = sparql_escape_string(revision.tutorials),
              how_to_guides = sparql_escape_string(revision.how_to_guides),
              explanation = sparql_escape_string(revision.explanation),
              reference = sparql_escape_string(revision.reference),

          )

          if init:
            query_string_revisions = replace_to_insert(query_string_revisions)

          update(query_string_revisions)
        
