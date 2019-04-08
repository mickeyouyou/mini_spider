#!/usr/bin/env python

"""
test 
"""
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from config_load import Loader

class TestConfigLoad(unittest.TestCase):
    """
    test config
    """

    def test_config_load(self):
        """
        test load
        """
        load = Loader("spider.conf")
        config = load.load_config()

        self.assertTrue(config['url_list_file'], './urls')
        self.assertTrue(config['output_directory'], './output')


if __name__ == '__main__':
    unittest.main()