# -*-coding:utf=8 -*-
import os
import sqlite3

class StatusDatabase():
    def __init__(self):
        self.db_name = os.path.join(os.getcwd(),'database','status.db')
        self.schema_file_name = os.path.join(os.getcwd(),'database','create_status_database.sql')
        #判断数据库是不是新的
        self.is_new = not os.path.exists(self.db_name)
        #创建数据库connect
        self.db_connect = sqlite3.connect(self.db_name)
        #创建数据库游标cursor
        self.cursor = self.db_connect.cursor()

        if self.is_new:
            self.__create_db()

    def __create_db(self):
        with open(self.schema_file_name,'r') as f:
           com_str = f.read()
        self.cursor.executescript(com_str)

    def delete_db(self):
        self.db_connect.close()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def reset_db(self):
        self.delete_db()
        self.__create_db()


if __name__ == '__main__':
    test_database = StatusDatabase();
    test_database.delete_db()