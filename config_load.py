#!/usr/bin/env python

"""
config load class
"""
import os
import sys
import logging
import configparser
from logger import Logger

SPIDER_ROOT = os.path.join(os.path.dirname(__file__), '.')

class Loader(object):
    """
    config loader class
    """
    def __init__(self, config_file="spider.conf"):
        """init config directory checkout"""
        Logger.config(
            log_file=os.path.join(SPIDER_ROOT, 'log/config_load.log'),
            use_stdout=True,
            log_level=logging.DEBUG)
        self.logger = Logger.get_logger(tag="Config_Loader")
        self.logger.info('Init logger')
        self.config = ''

        try:
            file_handler = open(config_file, 'r')
        except IOError:
            self.logger.error("Cannot find file: " + config_file)
            sys.exit(1)
        file_handler.close()
        self.config_file = config_file

    def load_config(self):
        """load config file"""
        config = configparser.RawConfigParser()
        config.read(self.config_file)
        self.config = config

        return self.config['spider']
