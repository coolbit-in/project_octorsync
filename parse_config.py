# -*- coding:utf=8 -*-
import ConfigParser

config_file = ConfigParser.ConfigParser()
config_file.read('config.ini')

class OctoRsyncConfigArgs():
    def __init__(self):

