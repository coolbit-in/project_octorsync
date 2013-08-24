#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
class Aa(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print self.name + '\n'

if __name__ == '__main__':
    a = Aa('old')
    a.start()
    a.join()
    print a.name