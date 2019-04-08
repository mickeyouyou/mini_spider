#!/usr/bin/env python

"""
web page parse class
"""
import os
import re
import urllib
import logging
import requests

from bs4 import BeautifulSoup

from logger import Logger

SPIDER_ROOT = os.path.join(os.path.dirname(__file__), '.')

class Parser(object):
    """
    url parse class object
    """
    def __init__(self, crawl_timeout):
        """
        init function
        """
        # request url
        self.url = ""
        self.pattern_target_url = ""
        self.crawl_timeout = crawl_timeout

        Logger.config(
            log_file=os.path.join(SPIDER_ROOT, 'log/webpage_parse.log'),
            use_stdout=True,
            log_level=logging.DEBUG)

        self.logger = Logger.get_logger(tag="Parser")

    def parse(self, url, pattern_target_url):
        """
        url
        patter_target_url
        crawl_timeout
        """
        self.logger.info("Start crawl the url:" + url)
        self.url = url
        try:
            res = requests.get(url, timeout=self.crawl_timeout)
        except requests.exceptions.Timeout:
            self.logger.error('Time out when crawl url: %s' % url)
            return
        res.encoding = 'utf-8'
        # case res.status_code not 200:
        if res.status_code != requests.codes.ok:
            self.logger.error(('This url: %s return the not ok status: %d') \
                % (url, res.status_code))

        soup = BeautifulSoup(res.text, features="html.parser")

        self.pattern_target_url = pattern_target_url
        a_elements = soup.find_all(href=re.compile(pattern_target_url))

        return self.task(a_elements)

    def task(self, elements):
        """
        process link address to simple
        """
        filtered_elements = []
        for link in elements:
            if link is None:
                continue
            href = link.get('href')

            # for filter page 1212.com when crawl sina.com.cn
            domain = urllib.parse.urlparse(href)
            if domain.netloc:
                if domain.netloc.split(".")[-3] != self.url.split(".")[1:3][0]:
                    continue

            if href.startswith("http://") or href.startswith("https://"):
                filtered_elements.append(href)
            else:
                #url_temp = urllib.parse.urljoin(self.url, href)
                filtered_elements.append("%s/%s" % (self.url, href))

        self.logger.info("parsed url:%s" % filtered_elements)

        return filtered_elements
