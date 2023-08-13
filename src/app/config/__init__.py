"""Utilities to load & apply the client-side config"""

from .read_conf_file import read_config
from .categories import categories_from_conf
from .overrides import apply_overrides