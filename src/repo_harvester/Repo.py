"""Contains the Repo class"""



# Built-in imports
from os.path import join, exists
from pathlib import Path
from typing import Any, List, Dict

# Relative imports
from .reposource import Reposource
from .config import apply_overrides, categories_from_conf
from .utils import TMP_REPOHARVESTER
from .Category import Category
from .Revision import Revision

# Package imports
from git import Repo as GitRepo, TagReference, HEAD, Reference

class Repo():
    """
    This class holds repository data that we want to export,
    as well as functions to get contents from the repository in question

    Important factors to consider when changing this class:
        - Universal: they are platform agnostic
        - Relevant: as good as all properties in these classes
                    are there because they are to be saved into the triplestore
    """
    def __init__(self, 
                 reposource: Reposource, 
                 name: str=None, 
                 description: str=None, 
                 repo_url: str=None, 
                 homepage_url: str=None, 
                 category_data: Any=None,
                 other_data: Any=None,
                 categories:Dict[str, Category]=categories_from_conf,
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
        """Returns the location where the repository would be/is cloned"""
        return Path(join(self.clone_parent_dir, self.name + "/"))
    
    @property
    def GitPython(self) -> GitRepo:
        """
        Returns the GitPython.Repo object for this repository.
        If that object doesn't exist already self.clone_files() will be run,
        after which the object will exist and be added 

        This in-between property getter allows repos to be cloned only
        when necessary, by not requiring clone_files on init; yet ensuring
        that any data from the clone in particular will be returned if asked
        """

        if hasattr(self, "_GitPython"):
            return self._GitPython
        else:
            self.clone_files()
            return self.GitPython

    

    @property
    def tags(self) -> List[str]:
        """Returns the repository tags"""
        return [tag.name for tag in self.GitPython.tags]


    def clone_files(self):
        """
        - (If it doesn't already exist) Clones the repository
        - Run git fetch & pull
        - Determine default branch
        """
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
        """
        Helper function for _checkout; allows finding exactly 1 result from
        GitPython.Repo.{branches/heads/tags/refs}
        """
        targets = [target for target in possible_targets if target.name.endswith(target_name)]
        if len(targets) > 1:
            raise ValueError("Multiple checkout targets for " + target_name)
        elif len(targets) == 1:
            return targets[0]
        else:
            return None


    def checkout(self, checkout_target:str=None):
        """Git checkout target branch/tag/head/ref"""
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
        """
        Helper function to handle version params.
        If the version param...
        - ... is defined, checkout that target
        - ... is undefined/None, the default branch will be explicitly checked out

        This way functions that (for example) read file contents can be sure
        there isn't an incorrect version checked out due to a previous command
        """

        if version:
            self.checkout(version)
        else:
            self.checkout(self.default_branch or "main" or "master")
    
    

    def get_file_path(self, filename, version=None):
        """
        When given a filename, return the path to the file from the local clone directory.

        If version is defined, attempt to checkout the passed tag/branch/...
        If version is None, will checkout to default_branch
        """
        self._set_version_or_default(version)
        return self.local_dir.joinpath(filename)


    def get_file_contents(self, path, version=None):
        """
        When given a filename, return the contents of the file from the local clone directory.

        If version is defined, attempt to checkout the passed tag/branch/...
        If version is None, will checkout to default_branch
        """
        try:
            with open(self.get_file_path(path, version), "r") as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return None    
    
    @property
    def image(self):
        """Returns the Image object for this repository"""
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

