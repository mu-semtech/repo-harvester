import unittest

from os import remove, path, environ
from ...app.utils.request import clear_cache, _url_to_cachefile_path, TMP_REPOHARVESTER, _get_from_cache, request, contents, json
from ..helpers import test_file_at


test_url = "https://hub.docker.com/_/alpine"
test_url_expected_output_path = TMP_REPOHARVESTER + "https-hub-docker-com-alpine.json"

class TestUtilsRequest(unittest.TestCase):

    def setUp(self) -> None:
        clear_cache()
        environ["RH_CACHE"] = ""

    def tearDown(self) -> None:
        environ["RH_CACHE"] = ""
        pass

    
    def test_url_to_cachefile_path(self):
        generated_path = _url_to_cachefile_path("https://hub.docker.com/_/alpine")
        self.assertEqual(generated_path, test_url_expected_output_path)
    
    def test_url_to_cachefile_path_custom_path_and_extension(self):
        generated_path = _url_to_cachefile_path("https://hub.docker.com/_/alpine", "html", "/tmp/repo-harvester-2/")
        custom_path = "/tmp/repo-harvester-2/https-hub-docker-com-alpine.html"
        self.assertEqual(generated_path, custom_path)
    
    def test_get_from_cache(self):
        # No parameters
        test_file_at(test_url_expected_output_path, "TEST-1")
        self.assertEqual(
            _get_from_cache(test_url),
            "TEST-1")
        
        # With extension
        test_file_at(test_url_expected_output_path.replace(".json", ".txt"), "TEST-2")
        self.assertEqual(
            _get_from_cache(test_url, extension="txt"),
            "TEST-2")
        
        # With extension and custom cache path
        custom_cache = "/tmp/repo-harvester2/"
        custom_test_url_expected_output_path = test_url_expected_output_path.replace("repo-harvester", "repo-harvester2").replace(".json", ".txt")
        test_file_at(custom_test_url_expected_output_path, "TEST-3")

        self.assertEqual(
            _get_from_cache(test_url, extension="txt", cache_path=custom_cache),
            "TEST-3")

        clear_cache(custom_cache)
        
        


        # With cache_path


    
    def test_get_from_cache_non_existant(self):
        self.assertFalse(_get_from_cache(test_url))

    
    def test_request(self):
        content = request(test_url, cache=False).text
        self.assertTrue(content.startswith("<!DOCTYPE html>"))
        self.assertTrue(content.endswith("</html>"))
    
    def test_request_cache(self):
        request(test_url, cache=True)
        
        self.assertTrue(path.exists(test_url_expected_output_path))

        with open(test_url_expected_output_path, "r", encoding="UTF-8") as file:
            content = file.read()

        self.assertTrue(content.startswith("<!DOCTYPE html>"))
        self.assertTrue(content.endswith("</html>"))


    def test_contents(self):
        content = contents(test_url)

        self.assertTrue(content.startswith("<!DOCTYPE html>"))
        self.assertTrue(content.endswith("</html>"))
    
    def test_json(self):
        json_path = "https://raw.githubusercontent.com/github/opensource.guide/main/package.json"
        data = json(json_path)
        self.assertEqual(data["name"], "open-source-guide")

    def test_env_var_cache(self):
        return
        self.assertTrue()
        

if __name__ == "__main__":
    unittest.main()