#!/usr/bin/env python

"""
crawled url table
"""

class UrlTable(object):
    """
    url table
    """

    def __init__(self):
        """
        """
        self.crawled_url = []

    def get(self):
        """
        get the crawled_url
        """
        return self.crawled_url

    def set(self, url):
        """
        append url to the dict crawled_url
        """
        self.crawled_url.append(url)

    def num(self):
        """
        get num of the url
        """
        return len(self.crawled_url)
