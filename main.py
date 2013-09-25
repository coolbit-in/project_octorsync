#!/usr/bin/python
# -*-coding:utf=8 -*-
import os
import sys
import time
import shlex
import subprocess
import threading
from config_args import *
from send_mail import *
from make_log import *


#工作组
class WorkQueue():
    def __init__(self):
        self.queue = []

    #从列表中载入实例
    def load_items(self, items):
        for item in items:
            self.queue.append(item)

    #封装了一下 len 函数,求队列长度
    def len(self):
        return len(self.queue)

#控制系统
class Controler():
    def __init__(self, queue):
        self.queue = queue
        self.busy_num = 0

    #每3秒在 status.log 中更新同步情况
    def __log(self):
        while True:
            self.log_file = open(os.path.join(LOG_ADDR, 'status.log'), 'w', 0)
            sys.stdout = self.log_file
            print time.asctime()
            print 'Busy:%d' % self.busy_num + '   ' + 'Idle:%d' % \
                   (self.queue.len() - self.busy_num)
            for item in self.queue.queue:
                print item.name + '   ' + item.status + '   ' + item.last_rsync_time + '   ' + item.last_rsync_status
            self.log_file.close()
            time.sleep(3)

    #从工作组中依次运行实例
    def run(self):
        for item in self.queue.queue:
            item.setDaemon(True)
            item.start()
        #调用 __log 方法实现死循环
        self.__log()

class DistroRsync(threading.Thread):
    def __init__(self, name, command_line, queue, controler, status_log):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.controler = controler
        # shlex.split() 的作用是分解命令字符串为列表
        self.args = shlex.split(command_line)
        self.status = 'idle'
        # last_rsync_time 是最后更新时间戳，无论更新成败
        self.last_rsync_time = time.asctime()
        # last_rsync_status 是最后一次更新的结果,success/fail
        self.last_rsync_status = 'fail'
        self.rsynced_times = 0
        self.waiting_time = WAITING_TIME
        self.log_file = ''
        self.status_log = status_log

    def __set_date_log(self):
        date_log_path = os.path.join(LOG_ADDR, time.strftime('%Y'), time.strftime('%m'),
                                     time.strftime('%d'))
        if not os.path.exists(date_log_path):
            os.makedirs(date_log_path)
        self.log_file = open(os.path.join(date_log_path, self.name + '.log'), 'a', 0)




    #部分变量的重新初始化
    def __re_init(self):
        self.status_log.info(self.name, 'Set status: idle')
        self.rsynced_times = 0
        self.status = 'idle'
        self.waiting_time = WAITING_TIME
        self.controler.busy_num -= 1
        self.log_file.close()

    #单次执行 rsync 的方法
    def __rsync_process(self):
        self.log_file.write('>>>>>>>>>>>>>> %s' % time.asctime() + ' >>>>>>>>>>>>\n')
        #retcode 是 rsync 进程的退出代码
        retcode = subprocess.call(self.args,
                                  stdout = self.log_file,
                                  stderr = self.log_file)
        # rsync 实行次数+1
        self.rsynced_times += 1
        #若 retcode == 0 则说明 rsync 正确执行
        return retcode

    #单次进行同步的过程:
    def __work(self):
        self.status = 'busy'
        self.status_log.info(self.name, 'Begin to synchronize. Set status: busy')
        while self.rsynced_times < MAX_ERROR_TIMES:
            #如果单次 rsync 成功，则结束单次同步
            retcode = self.__rsync_process()
            if not retcode:
                self.status_log.info(self.name, 'Rsync successfully')
                self.last_rsync_status = 'success'
                break
            #如果 rsync 失败次数 == MAX_ERROR_TIMES 表明同步失败，发邮件警报
            self.status_log.warn(self.name, 'Rsync failed, the exit code: %d' % retcode)

            if self.rsynced_times == MAX_ERROR_TIMES:
                #邮件服务下线，正在调试
                #send_mail = SendMail(msg = '%s had %d times rsync errors!\n'
                #                     % (self.name, MAX_ERROR_TIMES))
                #send_mail.send()

                self.log_file.write('octorsync:Sometime error, %d times\n'
                                    % MAX_ERROR_TIMES)

                self.status_log.error(self.name, 'Rsync error %d times, STOP to synchronize'
                                      % MAX_ERROR_TIMES)
                self.last_rsync_status = 'fail'

        #时间戳，无论成功还是失败
        self.last_rsync_time = time.asctime()

    #休眠过程
    def __sleep(self):
        time.sleep(self.waiting_time)

    #检查可否工作的过程，检查 self.controler.busy_num的值是否小于 MAX_BUSY_NUM
    #可启动返回0 ,不能启动返回1
    def __check(self):
        if self.controler.busy_num < MAX_BUSY_NUM:
            self.controler.busy_num += 1
            return 0
        else:
            return 1

    #等待过程，当 self.__check 失败后触发，每次触发等待时间减半，但不能小于 MIN_WATING_TIME
    def __wait(self):
        if self.waiting_time > MIN_WAITING_TIME:
            self.waiting_time = self.waiting_time / 2
        self.__sleep()

    #调用 实例的.start()时候，调用run()
    def run(self):
        while True:
            if not self.__check():
                self.__set_date_log()
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
    status_log = ServerLog()

    distro_ubuntu = DistroRsync(name = 'ubuntu',
                                command_line = UBUNTU_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)

    distro_deepin = DistroRsync(name = 'deepin',
                                command_line = DEEPIN_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)

    distro_qomo = DistroRsync(name = 'qomo',
                                command_line = QOMO_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)

    distro_gentoo = DistroRsync(name = 'gentoo',
                                command_line = GENTOO_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)

    distro_linuxmint = DistroRsync(name = 'linuxmint',
                                command_line = LINUXMINT_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)
    """
    distro_opensuse = DistroRsync(name = 'opensuse',
                                command_line = OPENSUSE_ARGS,
                                queue = work_queue,
                                controler = main_controler,
                                status_log = status_log)
    """
    work_queue.load_items([distro_ubuntu, distro_deepin, distro_qomo, distro_gentoo, distro_linuxmint])

    main_controler.run()
