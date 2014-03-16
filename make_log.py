# -*- coding:utf-8 -*-
import logging
import os
from parse_config import LOG_ROOT, MAIN_LOG_ADDR


class ServerLog():
    def __init__(self):
        if not os.path.exists(LOG_ROOT):
            os.makedirs(LOG_ROOT)
        self.main_log = logging.getLogger()
        self.main_log.setLevel(logging.DEBUG)

        self.log_file = logging.FileHandler(MAIN_LOG_ADDR)
        self.log_file.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        self.log_file.setFormatter(self.formatter)
        self.main_log.addHandler(self.log_file)

    def debug(self, name, message):
        self.main_log.debug('%s -- %s' % (name, message))

    def info(self, name, message):
        self.main_log.info('%s -- %s' % (name, message))

    def warn(self, name, message):
        self.main_log.warn('%s -- %s' % (name, message))

    def error(self, name, message):
        self.main_log.error('%s -- %s' % (name, message))
