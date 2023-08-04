# Native imports
from typing import Any, List
# Relative imports
from os.path import join
from .utils.request import contents, env_var_rh_cache_is_true, TMP_REPOHARVESTER
from .reposource.Reposource import Reposource
from .config.overrides import override_repo_values
from divio_docs_parser import DivioDocs
from git import Repo as GitRepo

try:
    from helpers import log
except ModuleNotFoundError:
    log = print
"""
Classes for repos and repo revisions.

Important factors about these classes:
- Universal: they are platform agnostic
- Relevant: as good as all properties in these classes
            are there because they are to be saved into the triplestore
"""

class Revision():
    """
    This class holds revision data
    
    This should be kept in line with app-mu-info/"""
    def __init__(self, image_tag: str, image_url: str, repo_tag: str, repo_url: str, readme: str) -> None:
        self.image_tag = image_tag
        self.image_url = image_url
        self.repo_tag = repo_tag
        self.repo_url = repo_url
        self.readme = str(readme)
        self.docs = DivioDocs(str(readme))


    @property
    def tutorials(self):
        return self.docs.tutorials
    
    @property
    def how_to_guides(self):
        return self.docs.how_to_guides
    
    @property
    def explanation(self):
        return self.docs.explanation
    
    @property
    def reference(self):
        return self.docs.reference
    


class Repo():
    """
    This class holds repository data that we want to export,
    as well as functions to get contents from the repository in question
    """
    def __init__(self, 
                 reposource: Reposource, 
                 name: str=None, 
                 description: str=None, 
                 repo_url: str=None, 
                 homepage_url: str=None, 
                 category_data: Any=None, 
                 other_data: Any=None,
                 clone_files=False,
                 clone_parent_dir=TMP_REPOHARVESTER) -> None:
        self.name = name
        self.description = description
        self.imagename = name

        self.tags = []

        self.repo_url = repo_url
        self.homepage_url = homepage_url
        
        self.reposource = reposource


        if category_data:
            self.category = self.reposource.parse_category(category_data)
        
        self.clone_parent_dir = clone_parent_dir

        # Data of any kind, in case it is needed
        self.other_data = other_data


        if clone_files:
            clone_files()

        #self = override_repo_values(self)
    
    @property
    def local_dir(self):
        return join(self.clone_parent_dir, self.name + "/")

    def clone_files(self):
        self.GitPython = GitRepo.clone_from(self.repo_url, self.local_dir)

        branches = [branch.name for branch in self.GitPython.branches]
        if False:  # TODO implement arg
            pass
        elif "main" in branches:
            self.default_branch = "main"
        elif "master" in branches:
            self.default_branch = "master"
        else:
            self.default_branch = branches[0]
        
    

    def get_file_path(self, filename, version=None):
        """When given a filename (and optionally version), return the files' url"""
        if version:
            self.GitPython.active_branch = version
        else:
            self.GitPython.active_branch = self.default_branch or "main" or "master"
    
    def get_file_contents(self, path, version=None, cache=env_var_rh_cache_is_true()):
        """Request a files contents. Automatically appends the repo url if a relative path is given"""
        if "http" not in path.lower():
            path = self.get_file_path(path, version)
        return contents(path, cache)
    
    
    @property
    def image(self):
        """Returns Image object for this repository"""
        return self.reposource.imagesource.get_image_by_name(self.imagename)


    @property
    def revisions(self) -> List[Revision]:
        return
        """Returns a list of Revisions for this repository"""
        revisions_list = []

        has_tags = len(self.tags) > 0
        has_images = len(self.image.tags) > 0
        
        if has_tags:
            image = self.image
            for repo_tag in self.tags:
                try:
                    if has_images:
                        stripped_repo_tag = repo_tag.lstrip("v").lstrip("V").lower()
                        image_tag = next(filter(lambda image_tag: image_tag.lower() == stripped_repo_tag , image.tags))

                    revisions_list.append(Revision(
                        image_tag if has_images else None,
                        image.imagesource.url_generator(image) if has_images else None,
                        repo_tag,
                        self.reposource.url_generator(self, repo_tag),
                        self.readme(False, repo_tag)
                    ))
                except StopIteration:
                    pass  # image_tag not found, pass
        else:
            revisions_list.append(Revision(
                None,
                None,
                self.name,
                self.reposource.url_generator(self),
                self.readme(False)
            ))
                
        print("Revisions: " + str(revisions_list))
        return revisions_list

    
    def readme(self, escaped=False, version=None):
        return
        """Returns the contents of the repository's README"""
        data = self.get_file_contents("README.md", version) 
        if escaped:
                # escape(Markup(
                #.replace("'", "&apos;")
                #.replace("*", "")   
                #))
            data = data\
                .replace("\\", "&bsol;")\
                .replace('"', "&quot;")\
                .replace("\n", "\\n")
        return data
    
    def __str__(self) -> str:
        return f"{self.name}@{self.repo_url}"

