# -*-coding:utf=8 -*-
import time
import os
#log的根目录
LOG_ADDR = os.path.join('/srv/log_new', time.strftime('%Y'), time.strftime('%m'),
                        time.strftime('%d'))
#软件源根目录
MIRROR_ADDR = '/srv/ftp/'

#单次出错重试次数
MAX_ERROR_TIMES = 5

#等待间隔(s)
WAITING_TIME = 60*60

#并行上限
MAX_BUSY_NUM = 2

#最小等待间隔(s)
MIN_WAITING_TIME = 30

UBUNTU_ARGS = 'rsync -6 -av --delete-after --ignore-errors --force -h' \
              + ' --exclude *ia64*' \
              + ' --exclude *powerpc*' \
              + ' --exclude *sparc*' \
              + ' --exclude *dapper*' \
              + ' --exclude *hardy*' \
              + ' --exclude *intrepid*' \
              + ' --exclude *jaunty*' \
              + ' --exclude *karmic*' \
              + ' --exclude *maverick*' \
              + ' --exclude *natty*' \
              + ' --exclude *oneiric*' \
              + ' --exclude *.iso' \
              + ' --exclude *.orig.tar.gz' \
              + ' --exclude *.diff.gz' \
              + ' --exclude *.dsc' \
              + ' rsync://mirrors6.ustc.edu.cn/ubuntu' \
              + MIRROR_ADDR + 'ubuntu'

DEEPIN_ARGS = 'rsync -6 -av -delete-after --ignore-errors --force -h' \
              + ' rsync://mirrors6.ustc.edu.cn/deepin' \
              + MIRROR_ADDR + 'deepin'