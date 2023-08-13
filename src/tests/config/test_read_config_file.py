import unittest

from os import remove, path
from ...repo_harvester.config.read_conf_file import read_config, CONFIG_DIR
from ..helpers import test_file_at
#from ..repo_harvester.config.overrides import override_repo_values

parameter_value = "Value"
test_conf_content = \
f"""[Configuration]
Parameter={parameter_value}
"""
test_conf_path = path.abspath("test.conf")

class TestConfig(unittest.TestCase):

    def setUp(self) -> None:
        test_file_at(test_conf_path, test_conf_content)

    def tearDown(self) -> None:
        remove(test_conf_path)

    
    def test_with_full_path(self):
        config = read_config(test_conf_path)

        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)

    def test_with_filename_without_suffix(self):
        filename = "test"
        path = CONFIG_DIR.joinpath(filename + ".conf")

        test_file_at(path, test_conf_content)
        
        config = read_config("test")
        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)
        
        remove(path)
    
    def test_with_filename_with_suffix(self):
        filename = "test"
        path = CONFIG_DIR.joinpath(filename + ".conf")

        test_file_at(path, test_conf_content)

        config = read_config("test.conf")
        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)

        remove(path)


if __name__ == "__main__":
    unittest.main()