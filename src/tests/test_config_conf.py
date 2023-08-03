import unittest

from os import remove, path
from ..app.config.conf import read_config, CONFIG_PATH
#from ..app.config.overrides import override_repo_values

parameter_value = "Value"
test_conf_content = \
f"""[Configuration]
Parameter={parameter_value}
"""
test_conf_path = path.abspath("test.conf")

def test_file_at(path):
    with open(path, "w") as file:
        file.write(test_conf_content)

class TestConfig(unittest.TestCase):

    def setUp(self) -> None:
        test_file_at(test_conf_path)

    def tearDown(self) -> None:
        remove(test_conf_path)

    
    def test_with_full_path(self):
        config = read_config(test_conf_path)

        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)

    def test_with_filename_without_suffix(self):
        filename = "test"
        path = CONFIG_PATH.joinpath(filename + ".conf")

        test_file_at(path)
        
        config = read_config("test")
        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)
        
        remove(path)
    
    def test_with_filename_with_suffix(self):
        filename = "test"
        path = CONFIG_PATH.joinpath(filename + ".conf")

        test_file_at(path)

        config = read_config("test.conf")
        self.assertEqual(config.get("Configuration", "Parameter"), parameter_value)

        remove(path)


if __name__ == "__main__":
    unittest.main()