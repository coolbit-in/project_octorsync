#!/usr/bin/python
# -*-coding:utf=8 -*-
import os
import sys
import time
import shlex
import subprocess
import threading
LOG_ADDR = '/Users/liusenyuan/computer/python/project_octorsync/logs/'
MIRROR_ADDR = ''

#单次出错重试次数
MAX_ERROR_TIMES = 5

#等待间隔
WAITING_TIME = 25

MAX_BUSY_NUM = 1

MIN_WAITING_TIME = 10
#工作组
class WorkQueue():
    def __init__(self):
        self.queue = []

    def load_items(self, items):
        for item in items:
            self.queue.append(item)

    def len(self):
        return len(self.queue)

#发射系统

#class Launcher(threading.Thread):
#    def __init__(self, queue):
#        threading.Thread.__init__(self)
#        self.queue = queue
#
#    def wait(self, time_now):
#        if time_now - self.processing_item.last_rsync_time < WAITING_TIME:
#            time.sleep(WAITING_TIME - (time_now - 
#                    self.processing_item.last_rsync_time));
#
#    def run(self):
#        while True:
#            #debug
#            print self.queue.len()
#            #debug end
#            if self.queue.len():
#                self.processing_item = self.queue.out_queue()
#                #debug
#                print self.processing_item.name
#                #debug
#                self.wait(time.time())
#                self.processing_item.start()
#            else:
#                time.sleep(10);


#控制系统
class Controler():
    def __init__(self, queue):
        self.queue = queue
        self.busy_num = 0

    def __log(self):
        while True:
            self.log_file = open(LOG_ADDR + 'status.log', 'w')
            sys.stdout = self.log_file
            print time.asctime()
            print 'Busy:%d' % self.busy_num + '   ' + 'Idle:%d' % \
                   (self.queue.len() - self.busy_num)
            for item in self.queue.queue:
                print item.name + '   ' + item.status
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
        self.last_rsync_time = time.time()
        self.rsynced_times = 0
        self.log_file = open(LOG_ADDR + name + '.log', 'a')
        self.waiting_time = WAITING_TIME

    def __re_init(self):
        self.rsynced_times = 0
        self.status = 'idle'
        self.waiting_time = WAITING_TIME
        self.controler.busy_num -= 1

    def __rsync_process(self):
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
        self.last_rsync_time == time.time()
        #self.receiver.run(self)

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
    print os.getpid()
    work_queue = WorkQueue()
    main_controler = Controler(queue = work_queue)

    distro_ubuntu = DistroRsync(name = 'ubuntu',
                                command_line = 'ls -al',
                                queue = work_queue,
                                controler = main_controler)

    distro_archlinux = DistroRsync(name = 'archlinux',
                                command_line = 'ls -al /',
                                queue = work_queue,
                                controler = main_controler)

    work_queue.load_items([distro_ubuntu, distro_archlinux])
    print work_queue.queue
    main_controler.run()
