# SPARQL query to update repos
SPARQL_STRING_REPO = """
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

# SPARQL query to update revisions
SPARQL_STRING_REVISION = """
DELETE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:RepoRevision; ext:revisionImageTag ?revisionImageTag; ext:revisionImageUrl ?revisionImageUrl; ext:revisionRepoTag ?revisionRepoTag; ext:revisionRepoUrl ?revisionRepoUrl; ext:readme ?readme; ext:tutorials ?tutorials; ext:howToGuides ?howToGuides; ext:explanation ?explanation; ext:reference ?reference; ext:hasRepo ?hasRepo.
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
    ext:tutorials {tutorials};
    ext:howToGuides {how_to_guides};
    ext:explanation {explanation};
    ext:reference {reference};
    
    ext:hasRepo {repograph}.
  }}
}} WHERE {{
  GRAPH <http://mu.semte.ch/application> {{
    {resource} a ext:RepoRevision.
    OPTIONAL {{ {resource} ext:hasRepo ?hasRepo }}
    OPTIONAL {{ {resource} ext:revisionRepoTag ?revisionRepoTag }}
    OPTIONAL {{ {resource} ext:revisionRepoUrl ?revisionRepoUrl }}
    OPTIONAL {{ {resource} ext:revisionImageTag ?revisionImageTag }}
    OPTIONAL {{ {resource} ext:revisionImageUrl ?revisionImageUrl }}
    OPTIONAL {{ {resource} ext:tutorials ?tutorials }}
    OPTIONAL {{ {resource} ext:how_to_guides ?how_to_guides }}
    OPTIONAL {{ {resource} ext:explanation ?explanation }}
    OPTIONAL {{ {resource} ext:reference ?reference }}
  }}
}}
"""
