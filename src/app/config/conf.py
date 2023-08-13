from configparser import ConfigParser
from pathlib import Path
from os.path import isfile, dirname



CONFIG_PATH = \
    Path(dirname(__file__)) \
    .parent\
    .parent\
    .parent\
    .joinpath("config/").absolute()
"""
Dynamically calculated. Set to `repo-harvester-root/config/`
"""

def read_config(filename: str, config_dir=CONFIG_PATH) -> ConfigParser:
    if not isfile(filename):
        if "." not in filename:
            filename += ".conf"

        path = config_dir.joinpath(filename)
        filename = str(path.absolute())
    #filename = Path(filename)
    config = ConfigParser()
    config.read(filename)
    return config
