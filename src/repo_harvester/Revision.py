# Package imports
from divio_docs_parser import DivioDocs

class Revision():
    """
    This class holds revision data.
    For information on what revisions are, see the relevant README discussion
    
    This should be kept in line with mu-semtech/app-mu-info
    """
    def __init__(self, image_tag: str, image_url: str, repo_tag: str, repo_url: str, path_to_repo: str, readme: str=None) -> None:
        self.image_tag = image_tag
        self.image_url = image_url
        self.repo_tag = repo_tag
        self.repo_url = repo_url
        self.readme = readme
        self.docs = DivioDocs(input_string_or_path=path_to_repo, embed_relative_files=True)


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
    
    def _joined(self, section: str):
        output = ""
        for key, value in getattr(self, section).items():
            output += value + "\n\n"
        
        return output
    
    @property
    def tutorials_as_string(self):
        return self._joined("tutorials")
    
    @property
    def how_to_guides_as_string(self):
        return self._joined("how_to_guides")
    
    @property
    def explanation_as_string(self):
        return self._joined("explanation")
    
    @property
    def reference_as_string(self):
        return self._joined("reference")
    