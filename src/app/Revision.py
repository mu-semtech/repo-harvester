from divio_docs_parser import DivioDocs

class Revision():
    """
    This class holds revision data
    
    This should be kept in line with app-mu-info/"""
    def __init__(self, image_tag: str, image_url: str, repo_tag: str, repo_url: str, path_to_repo: str) -> None:
        self.image_tag = image_tag
        self.image_url = image_url
        self.repo_tag = repo_tag
        self.repo_url = repo_url
        self.docs = DivioDocs(input_string_or_path=path_to_repo)


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
    