#!/usr/bin/env python

"""
crawled url table
"""
import os
import sys
import urllib
import unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from webpage_save import Saver


class TestWebpageSaver(unittest.TestCase):
    """
    test result save
    """

    def test_save(self):
        """
        save result
        """
        saver = Saver("output")

        dict = {'http://pycm.baidu.com:8081': [
        'http://pycm.baidu.com:8081/page1.html',
        'http://pycm.baidu.com:8081/page2.html', 
        'http://pycm.baidu.com:8081/page3.html', 
        'http://pycm.baidu.com:8081/mirror/index.html']}
        saver.save(dict)

        dir = "/Users/fengzongbao/codes/goodcoder/output/http%3A%2F%2Fpycm.baidu.com%3A8081"
        self.assertTrue(os.path.exists(dir))


if __name__ == '__main__':
    unittest.main()