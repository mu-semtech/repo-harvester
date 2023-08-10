# Native imports
from typing import Any, List, Dict
# Relative imports
from os.path import join, exists
from .Category import Category
from .utils.categories import categories
from .utils.request import contents, env_var_rh_cache_is_true, TMP_REPOHARVESTER
from .reposource.Reposource import Reposource
from .config.overrides import override_repo_values
from git import Repo as GitRepo, TagReference, HEAD, Reference
from pathlib import Path
from .Revision import Revision

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
                 categories:Dict[str, Category]=categories,
                 clone_files=False,
                 clone_parent_dir=TMP_REPOHARVESTER) -> None:
        self.name = name
        self.description = description
        self.imagename = name

        self.repo_url = repo_url if repo_url != "" else None
        self.homepage_url = homepage_url if homepage_url != "" else None
        
        self.reposource = reposource


        if category_data:
            self.category = self.reposource.parse_category(category_data, categories)
        
        self.clone_parent_dir = clone_parent_dir

        # Data of any kind, in case it is needed
        self.other_data = other_data


        if clone_files:
            self.clone_files()
        
        #self = override_repo_values(self)
    
    @property
    def local_dir(self):
        return Path(join(self.clone_parent_dir, self.name + "/"))
    
    @property
    def GitPython(self) -> GitRepo:
        if hasattr(self, "_GitPython"):
            return self._GitPython
        else:
            self.clone_files()
            return self.GitPython

    

    @property
    def tags(self) -> List[str]:
        return [tag.name for tag in self.GitPython.tags]


    def clone_files(self):
        if self.local_dir.exists():
            self._GitPython = GitRepo(self.local_dir)
        else:
            self._GitPython = GitRepo.clone_from(self.repo_url, self.local_dir)
        for remote in self.GitPython.remotes:
            remote.fetch()
            remote.pull()
            
        

        branches = [branch.name for branch in self.GitPython.branches]
        if False:  # TODO implement arg
            pass
        elif "main" in branches:
            self.default_branch = "main"
        elif "master" in branches:
            self.default_branch = "master"
        else:
            self.default_branch = branches[0]
        

    def _get_target_from(self, target_name: str, possible_targets: list):
        targets = [target for target in possible_targets if target.name.endswith(target_name)]
        if len(targets) > 1:
            raise ValueError("Multiple checkout targets for " + target_name)
        elif len(targets) == 1:
            return targets[0]
        else:
            return None


    def checkout(self, checkout_target:str=None):
        branch: HEAD = self._get_target_from(checkout_target, self.GitPython.branches)
        if branch is not None:
            return branch.checkout()
        
        head: HEAD = self._get_target_from(checkout_target, self.GitPython.heads)
        if head is not None:
            return head.checkout()

        tag: TagReference = self._get_target_from(checkout_target, self.GitPython.tags)
        if tag is not None:
            return self.GitPython.git.execute(["git", "checkout", checkout_target])
            #return tag.reference.checkout()
        #target: Reference = self._get_target_from(checkout_target, self.GitPython.references)

        reference: Reference = self._get_target_from(checkout_target, self.GitPython.refs)
        if reference is not None:
            return reference.checkout()


        raise ValueError("Ref " + checkout_target + " not found!")
        
        
    def _set_version_or_default(self, version=None):
        if version:
            self.checkout(version)
        else:
            self.checkout(self.default_branch or "main" or "master")
    
    

    def get_file_path(self, filename, version=None):
        """When given a filename (and optionally version), return the files' url"""
        self._set_version_or_default(version)
        return self.local_dir.joinpath(filename)


    def get_file_contents(self, path, version=None):
        """Request a files contents. Automatically appends the repo url if a relative path is given"""
        try:
            with open(self.get_file_path(path, version), "r") as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return None    
    
    @property
    def image(self):
        """Returns Image object for this repository"""
        return self.reposource.imagesource.get_image_by_name(self.imagename)


    def revisions(self) -> List[Revision]:
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
                        self.get_file_contents("README.md", repo_tag)
                    ))
                except StopIteration:
                    pass  # image_tag not found, pass
        else:
            revisions_list.append(Revision(
                None,
                None,
                self.name,
                self.reposource.url_generator(self),
                self.get_file_contents("README.md")
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

