# -*-coding:utf=8 -*-
import os

#log的根目录
LOG_ADDR = '/srv/log_new'
STATUS_LOG = os.path.join(LOG_ADDR, 'status_log')
STATUS_LOG_FILE = os.path.join(STATUS_LOG, 'main.log')

#软件源根目录
MIRROR_ADDR = '/srv/ftp/'

#单次出错重试次数
MAX_ERROR_TIMES = 5

#等待间隔(s)
WAITING_TIME = 60*60*2

#并行上限
MAX_BUSY_NUM = 4

#最小等待间隔(s)
MIN_WAITING_TIME = 30

UBUNTU_ARGS = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
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
              + ' ' + MIRROR_ADDR + 'ubuntu'

DEEPIN_ARGS = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
              + ' rsync://mirrors6.ustc.edu.cn/deepin' \
              + ' ' + MIRROR_ADDR + 'deepin'

GENTOO_ARGS = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
              + ' rsync://mirrors6.ustc.edu.cn/gentoo' \
              + ' ' + MIRROR_ADDR + 'gentoo'

QOMO_ARGS   = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
              + ' --exclude *.iso' \
              + ' --exclude *.iso*' \
              + ' rsync://mirrors6.ustc.edu.cn/qomo' \
              + ' ' + MIRROR_ADDR + 'qomo'

LINUXMINT_ARGS = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
              + ' --exclude *.iso' \
              + ' --exclude *.iso*' \
              + ' --exclude *.~tmp~*' \
              + ' rsync://mirrors6.ustc.edu.cn/linuxmint' \
              + ' ' + MIRROR_ADDR + 'linuxmint'

OPENSUSE_ARGS = 'rsync -6 -av --delete-after --ignore-errors --timeout=3600 --force -h' \
              + ' rsync://mirrors6.ustc.edu.cn/opensuse' \
              + ' --exclude *.iso' \
              + ' ' + MIRROR_ADDR + 'opensuse'


