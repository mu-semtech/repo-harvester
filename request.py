from os import makedirs
from os.path import join, exists
from json import loads
from requests import get
from slugify import slugify
from time import sleep

cache_dir = "cache/"
makedirs(cache_dir, exist_ok=True)

def url_to_filename(url, extension="json"):
    return join(cache_dir, slugify(url) + "." + extension)

def get_from_cache(url):
    file = url_to_filename(url)

    if exists(file):
        with open(file, "r", encoding="UTF-8") as file:
            data = file.read()
        
        return data
    else:
        return False

def request(url):
    data = get(url)
    with open(url_to_filename(url), "w", encoding="UTF-8") as file:
        file.write(data.text)

    return data

def json(url, timeout_if_not_cached=0):
    data = get_from_cache(url)
    if data:
        return loads(data)
    else:
        data = request(url)
        if timeout_if_not_cached > 0:
            print(f"Timeout passed! Sleeping for {timeout_if_not_cached}")
            sleep(timeout_if_not_cached)
        return data.json()
            
