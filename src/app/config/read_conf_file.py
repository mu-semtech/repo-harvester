"""Defines helper method to read config files, as well as the default config location"""

from os.path import isfile, dirname
from configparser import ConfigParser
from pathlib import Path


CONFIG_DIR = \
    Path(dirname(__file__)) \
    .parent\
    .parent\
    .parent\
    .joinpath("config/").absolute()
"""The directory to look in for *.conf files. Dynamically calculated, set to `repo-harvester-root/config/`"""

def read_config(filename: str, config_dir=CONFIG_DIR) -> ConfigParser:
    """
    Returns a ConfigParser with the passed config file read into it.

    - If passed a direct path, read that file
    - If passed a stem + suffix (e.g. "categories.conf"), load from config_dir 
    - If passed a stem (e.g. "categories"), add .conf & load from config_dir
    """
    if not isfile(filename):
        if "." not in filename:
            filename += ".conf"

        path = config_dir.joinpath(filename)
        filename = str(path.absolute())
    config = ConfigParser()
    config.read(filename)
    return config
