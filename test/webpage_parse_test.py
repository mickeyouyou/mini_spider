#!/usr/bin/env python

"""
crawled url table
"""
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from webpage_parse import Parser


class TestWebpageParse(unittest.TestCase):
    """
    parse 
    """

    def test_parse(self):
        """
        test parse
        """
        # with timeout 3
        parser = Parser(3)
        a_elements = parser.parse('http://pycm.baidu.com:8081', ".*.(htm|html)$")

        self.assertTrue(len(a_elements), 4)

if __name__ == '__main__':
    unittest.main()