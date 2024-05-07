import unittest
import os
from sshconfig import SSHConfig

parent_dir = os.path.split(__file__)[0]
resources = os.path.join(parent_dir, "resources")

class TestSSHConfig(unittest.TestCase):
    
    def setUp(self):
        filepath = os.path.join(resources, "test_config")
        self.config = SSHConfig(filepath)

    def test_read(self):
        hosts = self.config.read()
        self.assertEqual(len(hosts), 4)

        host_names = [x.host for x in hosts]
        self.assertListEqual(host_names, ["*", "*.example.com", "*.com", "quick"])