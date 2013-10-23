# -*- coding:utf-8 -*-
import ConfigParser

config_file_parser = ConfigParser.SafeConfigParser()
config_file_parser.read('config.ini')

global_args = dict(config_file_parser.items('global'))

LOG_ROOT = global_args['log_root']

MIRROR_ROOT = global_args['mirror_root']

STATUS_LOG_ADDR = global_args['status_log_addr']

MAIN_LOG_ADDR = global_args['main_log_addr']

MAX_ERROR_TIMES = int(global_args['max_error_times'])

WAITING_TIME = int(global_args['waiting_time'])

MIN_WAITING_TIME = int(global_args['min_waiting_time'])

MAX_BUSY_NUM = int(global_args['max_busy_num'])

RSYNC_BASE_6 = global_args['rsync_base_6']

RSYNC_BASE_4 = global_args['rsync_base_4']

#print [LOG_ROOT, MIRROR_ROOT, MAX_BUSY_NUM, WAITINT_TIME, MIN_WAITNG_TIME,\
#       MAX_BUSY_NUM, RSYNC_BASE_4, RSYNC_BASE_6, STATUS_LOG_ADDR, MAIN_LOG_ADDR]
#print global_args
#for item in config_file_parser.sections()[1:]:
distro_args = dict((section_name, dict((key, value) for (key, value) in config_file_parser.items(section_name))) \
           for section_name in config_file_parser.sections()[1:])
