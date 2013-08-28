#!/usr/bin/env python
# -*- coding:utf=8 -*-
import os
import smtplib
import time
#from email.message import Message
from email.mime.text import MIMEText
from email.header import Header

class SendMail():
    def __init__(self, msg = ''):
        self.account_file = open(os.path.join(os.getcwd(), 'account.txt'), 'r')
        self.username = self.account_file.readline().replace('\n', '')
        self.password = self.account_file.readline().replace('\n', '')
        self.from_addr = self.username
        self.to_addr = 'coolbit.in@gmail.com'
        self.smtp_server = 'smtp.gmail.com'
        self.text_file = open(os.path.join(os.getcwd(), 'mail.txt'), 'r')
        self.msg  = msg

    def send(self):
        if msg == '':
            message = MIMEText(self.text_file.read(), 'plain', 'utf-8')
            message['Subject'] = Header('Warning! Form linux.xidian.edu.cn')
            message_string = message.as_string()
        else:
            message_string = self.msg

        smtp_con = smtplib.SMTP(self.smtp_server, port = 587, timeout = 30)
        smtp_con.set_debuglevel(1)
        smtp_con.starttls()
        smtp_con.login(self.username, self.password)
        smtp_con.sendmail(self.from_addr, self.to_addr, message_string)
        time.sleep(5)
        smtp_con.quit()

if __name__ == '__main__':
    test_mail = SendMail()
    test_mail.send()

