import unittest
import os
from sshconfig import regex, SSHConfig, get_alias

parent_dir = os.path.split(__file__)[0]
resources = os.path.join(parent_dir, "resources")

class TestRegex(unittest.TestCase):

    def test_wildcards(self):
        sh_pattern = "file*.txt"
        re_pattern = "file.*\.txt"
        self.assertEqual(regex(sh_pattern), re_pattern)

        sh_pattern = "myfile?.log"
        re_pattern = "myfile.\.log"
        self.assertEqual(regex(sh_pattern), re_pattern)

    def test_brackets(self):
        sh_pattern = "file[123].txt"
        re_pattern = "file[123]\.txt"
        self.assertEqual(regex(sh_pattern), re_pattern)


class TestGetters(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(resources, "test_config")
        self.config = SSHConfig(filepath)

    def test_get_alias(self):
        alias = get_alias("test.case.edu", self.config.filepath)
        self.assertEqual(alias, "quick")

        alias = get_alias("non.existent.com")
        self.assertIsNone(alias)

    
if __name__ == "__main__":
    unittest.main()