"""Helper functions to handle requests & caching"""

# Built-in imports
from os import makedirs, environ
from os.path import join, exists
from json import loads
from time import sleep
from shutil import rmtree
from typing import Union

# Relative imports
from ..utils import log

# Package imports
from requests import get, Response
from slugify import slugify

TMP_REPOHARVESTER = "/tmp/repo-harvester/"
def env_var_rh_cache_is_true() -> bool:
    """Returns True if the RH_CACHE environment variable is defined"""
    return bool(environ.get("RH_CACHE"))

def create_cache(cache_path=TMP_REPOHARVESTER):
    """Creates directory at cache_path. Defaults to /tmp/repo-harvester"""
    makedirs(cache_path, exist_ok=True)

def clear_cache(cache_path=TMP_REPOHARVESTER):
    """Removes directory at cache_path. Defaults to /tmp/repo-harvester"""
    rmtree(cache_path, ignore_errors=True)

def _url_to_cachefile_path(url, cache_path=TMP_REPOHARVESTER) -> str:
    """Create a path from an URL. For use during caching"""
    return join(cache_path, slugify(url))

def _get_from_cache(url, cache_path=TMP_REPOHARVESTER) -> Union[str,bool]:
    """Read data from cachefile for specified url. Returns False if not cached"""
    file = _url_to_cachefile_path(url, cache_path)

    if exists(file):
        with open(file, "r", encoding="UTF-8") as file:
            data = file.read()
        
        return data
    else:
        return False

def request(url, cache=env_var_rh_cache_is_true(), cache_path=TMP_REPOHARVESTER) -> Response:
    """Send a request to the url, and cache the result. Returns requests.Response object"""
    data = get(url)
    if cache:
        if not exists(cache_path):
            create_cache(cache_path)
        with open(_url_to_cachefile_path(url, cache_path), "w", encoding="UTF-8") as file:
            file.write(data.text)

    return data

def contents(url, request_timeout=0, json=False, cache=env_var_rh_cache_is_true(), cache_path=TMP_REPOHARVESTER) -> any:
    """Get (raw|json) contents from specified url. Will use cache if exists"""
    data = _get_from_cache(url, cache_path) if cache else False
    if data:
        return loads(data) if json else data
    else:
        data = request(url, cache, cache_path)
        if request_timeout > 0:
            log("WARNING", f"Timeout passed! Sleeping for {request_timeout}")
            sleep(request_timeout)
        return data.json() if json else data.text

def json(url, request_timeout=0, cache=env_var_rh_cache_is_true(), cache_path=TMP_REPOHARVESTER):
    """Call the contents function, but always return parsed json"""
    return contents(url, request_timeout, json=True, cache=cache, cache_path=cache_path)
