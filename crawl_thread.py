#!/usr/bin/env python

"""
crawl thread function
"""

import os
import time
import logging
import threading

from logger import Logger
from webpage_save import Saver
from webpage_parse import Parser
from url_table import UrlTable

SPIDER_ROOT = os.path.join(os.path.dirname(__file__), '.')

lock = threading.Lock()

crawled_url = UrlTable()


class CrawlThread(threading.Thread):
    """
    based on threading.Thread
    """

    def __init__(self, config, queue):
        """
        constructor
        """
        threading.Thread.__init__(self)
        self.config = config
        self.queue = queue
        self.crawl_timeout = int(config['crawl_timeout'])
        self.crawl_interval = int(config['crawl_interval'])

        Logger.config(
            log_file=os.path.join(SPIDER_ROOT, 'log/crawl_thread.log'),
            use_stdout=True,
            log_level=logging.DEBUG)
        self.logger = Logger.get_logger(tag="CrawlThead")
        self.logger.info('Init logger')

    def run(self):
        """
        threading.Thread api run
        @parameter url, crawled_url, parent_depth
        """
        while not self.queue.empty():
            # get queue payload
            payload = self.queue.get()
            url = payload[0]
            parent_depth = payload[1]
            self.logger.debug("working with queue: %s, and with %s" % (payload, self.name))

            # page crawl max_depth check
            link_depth = parent_depth + 1
            if link_depth > int(self.config['max_depth']):
                self.logger.error("Touch the max depth: %s when crawled url %s" %
                                  (self.config['max_depth'], url))

            global crawled_url
            url_table = crawled_url.get()

            # check crawled_url
            # 多线程中的数据互斥访问, 使用threading.Lock()
            if lock.acquire():
                if url in url_table:
                    self.logger.error("This url have been crawled : %s" % url)

                # Parse url
                parser = Parser(self.crawl_timeout)
                a_elements = parser.parse(url, self.config['target_url'])

                url_dict = {}
                href = []
                if a_elements:
                    for link in a_elements:
                        self.queue.put([link, link_depth])
                        href.append(link)
                    url_dict[url] = href
                    page_save = Saver(self.config['output_directory'])
                    page_save.save(url_dict)
                    self.logger.debug("saved crawled data:%s" % url_dict)

                self.queue.task_done()

                crawled_url.set(url)
                self.logger.debug("updated crawled_url: %s" % crawled_url.get())
                lock.release()

            time.sleep(self.crawl_interval)
        self.queue.join()
