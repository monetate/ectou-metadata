#!/usr/bin/env python


try:
    from urllib2 import urlopen
except ImportError:
    from urllib import urlopen

import os
import subprocess
import time
import unittest


class TestMetadataApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        meta_service_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         "..", "ectou_metadata", "service.py"))
        test_host = "localhost"
        test_port = 4242

        cls.process = subprocess.Popen("python {} --host {} --port {}".format(meta_service_path, test_host, test_port),
                                       stdout=subprocess.PIPE, shell=True)
        time.sleep(1)
        cls.base_url = "http://{}:{}".format(test_host, test_port)

    @classmethod
    def tearDownClass(cls):
        cls.process.kill()

    def fetch(self, url):
        response = urlopen(url)
        return response.read().decode("utf-8")

    def test_root(self):
        self.assertEqual(self.fetch(self.base_url), "latest")

    def test_latest(self):
        self.assertEqual(self.fetch("{}/latest/".format(self.base_url)), "meta-data")

    def test_metadata(self):
        root_metadata = ("iam/\n"
                         "instance-id\n"
                         "local-ipv4\n"
                         "placement/\n"
                         "public-hostname\n"
                         "public-ipv4")
        self.assertEqual(self.fetch("{}/latest/meta-data/".format(self.base_url)), root_metadata)

    def test_placement(self):
        placement_metadata = "availability-zone"
        self.assertEqual(self.fetch("{}/latest/meta-data/placement/".format(self.base_url)), placement_metadata)


if __name__ == "__main__":
    unittest.main(verbosity=2)
