#!/usr/bin/env python

"""
web page saver class
"""

import os
import urllib.parse

class Saver(object):
    """
    web page saver class
    """
    def __init__(self, out_put_dir):
        """
        setter
        """
        self.out_put_dir = os.path.dirname(os.path.abspath(__file__)) + "/" + out_put_dir
        if not os.path.exists(self.out_put_dir):
            os.makedirs(self.out_put_dir)

    def save(self, data):
        """
        save result to files
        """
        for url, url_table in data.items():
            # for good file name, substring the raw url
            output_file = self.out_put_dir + "/" + urllib.parse.quote(url, '#')

            file_handler = open(output_file, 'w+')

            for sub_url in url_table:
                sub_url_detail = sub_url + '\n'
                file_handler.write(sub_url_detail)
            file_handler.close
