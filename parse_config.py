# -*- coding:utf=8 -*-
import ConfigParser

config_file_parser = ConfigParser.SafeConfigParser()
config_file_parser.read('config.ini')
global_args = dict(config_file_parser.items('global'))
for item in config_file_parser.sections()[1:]:



