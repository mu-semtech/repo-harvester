from configparser import ConfigParser
from pathlib import Path

def read_config(filename: str) -> ConfigParser:
    filename = Path(filename).stem
    config = ConfigParser()
    config.read(Path(__file__).parent.joinpath(f"config/{filename}.conf"))
    return config
