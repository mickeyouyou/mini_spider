#!/usr/bin/env python

"""
crawled url table
"""
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from url_table import UrlTable


class TestUrlTable(unittest.TestCase):
    """
    test url table
    """

    def test_set(self):
        """
        test set
        """
        url_table = UrlTable()
        url_table.set('www.baidu.com')
        url_table.set('www.baidu.com.cn')

        self.assertTrue(url_table.get)
        self.assertTrue('www.baidu.com' in url_table.get())
        self.assertFalse('www.baidu.cn' in url_table.get())
        self.assertTrue(url_table.num(), 2)


if __name__ == '__main__':
    unittest.main()