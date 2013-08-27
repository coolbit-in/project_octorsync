#!/usr/bin/python
# -*-coding:utf=8 -*-
import os
import sys
import time
import shlex
import subprocess
import threading
from config_args import *

#工作组
class WorkQueue():
    def __init__(self):
        self.queue = []

    def load_items(self, items):
        for item in items:
            self.queue.append(item)

    def len(self):
        return len(self.queue)

#控制系统
class Controler():
    def __init__(self, queue):
        self.queue = queue
        self.busy_num = 0

    def __log(self):
        while True:
            self.log_file = open(os.path.join(LOG_ADDR, 'status.log'), 'w', 0)
            sys.stdout = self.log_file
            print time.asctime()
            print 'Busy:%d' % self.busy_num + '   ' + 'Idle:%d' % \
                   (self.queue.len() - self.busy_num)
            for item in self.queue.queue:
                print item.name + '   ' + item.status + '   ' + item.last_rsync_time
            self.log_file.close()
            time.sleep(3)

    def run(self):
        for item in self.queue.queue:
            item.setDaemon(True)
            item.start()
        self.__log()

class DistroRsync(threading.Thread):
    def __init__(self, name, command_line, queue, controler):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.controler = controler
        self.args = shlex.split(command_line)
        self.status = 'idle'
        self.last_rsync_time = time.asctime()
        self.rsynced_times = 0
        self.waiting_time = WAITING_TIME
        #检测Log路径是否存在
        try:
            self.log_file = open(os.path.join(LOG_ADDR, name + '.log'), 'a', 0)
        except IOError:
            os.makedirs(LOG_ADDR)
            self.log_file = open(os.path.join(LOG_ADDR, name + '.log'), 'a', 0)

    def __re_init(self):
        self.rsynced_times = 0
        self.status = 'idle'
        self.waiting_time = WAITING_TIME
        self.controler.busy_num -= 1

    def __rsync_process(self):
        self.log_file.write('>>>>>>>>>>>>>> %s' % time.asctime() + ' >>>>>>>>>>>>\n')
        retcode = subprocess.call(self.args,
                                  stdout = self.log_file,
                                  stderr = self.log_file)
        self.rsynced_times += 1
        if retcode == 0:
            return 0
        else:
            return 1

    def __work(self):
        self.status = 'busy'
        while self.rsynced_times < MAX_ERROR_TIMES:
            if not self.__rsync_process():
                break
            if self.rsynced_times == MAX_ERROR_TIMES:
                self.log_file.write("octorsync:Sometime error, %d times\n" 
                                    % MAX_ERROR_TIMES)
        self.last_rsync_time = time.asctime()

    def __sleep(self):
        time.sleep(self.waiting_time)

    def __check(self):
        if self.controler.busy_num < MAX_BUSY_NUM:
            self.controler.busy_num += 1
            return 0
        else:
            return 1

    def __wait(self):
        if self.waiting_time > MIN_WAITING_TIME:
            self.waiting_time = self.waiting_time / 2
        self.__sleep()

    def run(self):
        while True:
            if not self.__check():
                self.__work()
                self.__re_init()
                self.__sleep()
            else:
                self.__wait()


if __name__ == '__main__':
    pid_log = open(os.path.join(os.getcwd(), 'octorsync.pid'), 'w')
    pid_log.write(str(os.getpid()))
    pid_log.close()
    work_queue = WorkQueue()
    main_controler = Controler(queue = work_queue)

    distro_ubuntu = DistroRsync(name = 'ubuntu',
                                command_line = UBUNTU_ARGS,
                                queue = work_queue,
                                controler = main_controler)

    distro_deepin = DistroRsync(name = 'deepin',
                                command_line = DEEPIN_ARGS,
                                queue = work_queue,
                                controler = main_controler)

    distro_qomo = DistroRsync(name = 'qomo',
                                command_line = QOMO_ARGS,
                                queue = work_queue,
                                controler = main_controler)

    distro_gentoo = DistroRsync(name = 'gentoo',
                                command_line = GENTOO_ARGS,
                                queue = work_queue,
                                controler = main_controler)

    work_queue.load_items([distro_ubuntu, distro_deepin, distro_qomo, distro_gentoo])

    main_controler.run()
