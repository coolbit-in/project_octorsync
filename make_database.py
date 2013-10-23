# -*-coding:utf-8 -*-
import os
import sqlite3
import threading
class StatusDatabase():
    def __init__(self):
        self.db_name = os.path.join(os.getcwd(),'database','status.db')
        self.schema_file_name = os.path.join(os.getcwd(),'database','create_status_database.sql')
        if self.is_db_exists():
           self.delete_db()
        #创建数据库连接
        self.db_connect = sqlite3.connect(self.db_name, check_same_thread = False)
        #创建数据库游标cursor
        self.cursor = self.db_connect.cursor()
        self.__create_db()
        self.db_lock = threading.Lock()
    def is_db_exists(self):
        if os.path.exists(self.db_name):
            return True
        else:
            return False

    def __create_db(self):
        with open(self.schema_file_name,'r') as f:
           com_str = f.read()
        self.cursor.executescript(com_str)

    def delete_db(self):
            os.remove(self.db_name)

    def reset_db(self):
        self.delete_db()
        self.__create_db()

    def insert_distro(self, name, time, status):
        # TODO 还没有做一些存在性判断
        if self.db_lock.acquire():
            self.cursor.execute("insert into octorsync_status (distro_name,last_rsync_time,rsync_status) \
                            values('%s','%s','%s')" % (name, time, status))
            self.db_connect.commit()
            print "insert %s success\n" % name
            self.db_lock.release()

    def update_last_rsync_time(self, name, time):
        if self.db_lock.acquire():
            self.cursor.execute("update octorsync_status set last_rsync_time='%s' where distro_name=='%s'"
                            % (time, name))
            self.db_connect.commit()
            self.db_lock.release()


    def update_status(self, name, status):
        if self.db_lock.acquire():
            self.cursor.execute("update octorsync_status set rsync_status='%s' where distro_name=='%s'"
                            % (status, name))
            self.db_connect.commit()
            self.db_lock.release()


if __name__ == '__main__':
    test_database = StatusDatabase();
    test_database.delete_db()