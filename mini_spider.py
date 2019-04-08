#!/usr/bin/env python

"""
mini spider function
"""

import os
import sys
import queue
import logging
import argparse

from logger import Logger
from config_load import Loader
from crawl_thread import CrawlThread


SPIDER_ROOT = os.path.join(os.path.dirname(__file__), '.')

FEED_ROOT_DEPTH = 0

class Spider(object):
    """
    mini webpage spider
    """
    def __init__(self):
        """
        init method
        """
        # config from spider.conf
        self.config = {}
        # list from key(urls) to crawled results, and save to file
        self.url_dict = []
        # crawl queue
        self.queue = queue.Queue(0)
        # crawl interval
        self.crawl_interval = 0

        self.crawl_timeout = 0

        Logger.config(
            log_file=os.path.join(SPIDER_ROOT, 'log/mini_spider.log'),
            use_stdout=True,
            log_level=logging.DEBUG)
        self.logger = Logger.get_logger(tag="Mini_Spider")
        self.logger.info('Init logger')

    def prepare(self):
        """
        prepare for the crawl action
        read feed file to the crawl queue
        """
        url_list_file = self.config['url_list_file']
        #url_file_handler = open(url_list_file, 'r')
        with open(url_list_file, 'r') as f:
            for line in f.readlines():
                url = line.strip()
                self.queue.put([url, FEED_ROOT_DEPTH])

    def queue_task(self):
        """
        queue task for page crawl
        """
        ThreadList = []
        for i in range(1, int(self.config['thread_count'])):
            t = CrawlThread(self.config, self.queue)
            ThreadList.append(t)

        for t in ThreadList:
            t.start()

        for t in ThreadList:
            t.join()

    def main(self):
        """
        main function
        """
        parser = argparse.ArgumentParser(
            description="""
            a mini spider based on config file and re.
            It can set deepth and timeout.""")

        parser.add_argument(
            "-c", action="store", type=str, help="config file",
            default="spider.conf")

        # just echo parameter for type store_true
        parser.add_argument(
            "-v",
            action="store_true",
            help="print the spider version")

        args = parser.parse_args()

        if args.v:
            print("Mini spider version v0.1")
            print("Developed from fengzongbao@baidu.com")
            sys.exit()

        if args.c:
            config_loader = Loader(args.c)
            self.config = config_loader.load_config()
            self.logger.debug("Loaded the config file: " + args.c)
            self.crawl_interval = int(self.config['crawl_interval'])
            self.crawl_timeout = int(self.config['crawl_timeout'])

        # prepare the urls
        self.prepare()
        # start thread for crawl
        self.queue_task()

if __name__ == '__main__':
    spider = Spider()
    spider.main()
    