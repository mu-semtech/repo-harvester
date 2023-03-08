# Native imports
from os import makedirs
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

cache_dir = "cache/"
makedirs(cache_dir, exist_ok=True)

def url_to_cachefile_path(url, extension="json") -> str:
    """Create a path from an URL. For use during caching"""
    return join(cache_dir, slugify(url) + "." + extension)

def get_from_cache(url) -> Union[str,False]:
    """Read data from cachefile for specified url. Returns False if not cached"""
    file = url_to_cachefile_path(url)

    if exists(file):
        with open(file, "r", encoding="UTF-8") as file:
            data = file.read()
        
        return data
    else:
        return False

def request(url) -> Response:
    """Send a request to the url, and cache the result. Returns requests.Response object"""
    data = get(url)
    with open(url_to_cachefile_path(url), "w", encoding="UTF-8") as file:
        file.write(data.text)

    return data

def contents(url, timeout_if_not_cached=0, json=False) -> any:
    """Get (raw|json) contents from specified url. Will use cache if exists"""

    data = get_from_cache(url)
    if data:
        return loads(data) if json else data
    else:
        data = request(url)
        if timeout_if_not_cached > 0:
            print(f"Timeout passed! Sleeping for {timeout_if_not_cached}")
            sleep(timeout_if_not_cached)
        return data.json() if json else data.content
            

def json(url, timeout_if_not_cached=0):
    """Call the contents function, but always return parsed json"""
    return contents(url, timeout_if_not_cached, True)
