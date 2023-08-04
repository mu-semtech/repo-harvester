# Native imports
from os import makedirs, environ
from os.path import join, exists
from json import loads
from time import sleep
from typing import Union
# Package imports
from requests import get, Response
from slugify import slugify

"""
Helper functions to handle requests & caching
"""

CACHE_ENABLED = environ["MODE"] == "development"

TMP_REPOHARVESTER = "/tmp/repo-harvester/"

if CACHE_ENABLED:
    makedirs(TMP_REPOHARVESTER, exist_ok=True)

def _url_to_cachefile_path(url, extension="json", cache_path=TMP_REPOHARVESTER) -> str:
    """Create a path from an URL. For use during caching"""
    return join(cache_path, slugify(url) + "." + extension)

def _get_from_cache(url) -> Union[str,bool]:
    """Read data from cachefile for specified url. Returns False if not cached"""
    file = _url_to_cachefile_path(url)

    if exists(file):
        with open(file, "r", encoding="UTF-8") as file:
            data = file.read()
        
        return data
    else:
        return False

def request(url, cache:bool=environ.get("RH_CACHE") is not None) -> Response:
    """Send a request to the url, and cache the result. Returns requests.Response object"""
    data = get(url)
    if cache:
        with open(_url_to_cachefile_path(url), "w", encoding="UTF-8") as file:
            file.write(data.text)

    return data

def contents(url, request_timeout=0, json=False) -> any:
    """Get (raw|json) contents from specified url. Will use cache if exists"""

    data = _get_from_cache(url) if CACHE_ENABLED else False
    if data:
        return loads(data) if json else data
    else:
        data = request(url)
        if request_timeout > 0:
            print(f"Timeout passed! Sleeping for {request_timeout}")
            sleep(request_timeout)
        return data.json() if json else data.text
            

def json(url, request_timeout=0):
    """Call the contents function, but always return parsed json"""
    return contents(url, request_timeout, True)
