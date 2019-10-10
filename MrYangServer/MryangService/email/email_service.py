import smtplib
import time
from email.mime.text import MIMEText

from MryangService.frames.base import BaseService
from frames import logger

MAX_TAG_CACHE_COUNT = 5  # 每一个tag的最多数量.


class ES(BaseService):

    def __init__(self):
        BaseService.__init__(self)
        self.send_cache_list = {}
        self.sender = '1702497572@qq.com'
        self.receivers = ['1226341090@qq.com']

    def append_send_list(self, content, tag, title='01-pc的通知'):
        if tag not in self.send_cache_list:
            self.send_cache_list[tag] = []
            pass
        tag_list = self.send_cache_list.get(tag)
        if len(tag_list) > MAX_TAG_CACHE_COUNT:
            del tag_list[0]
        tag_list.append((title, content))
        self.set()  # 启动loop

    def __send(self, content, tag, title='01-pc的通知'):
        try:
            smtpObj = smtplib.SMTP_SSL(host='smtp.qq.com')
            smtpObj.connect(host='smtp.qq.com', port=465)
            smtpObj.login(self.sender, 'qjmrhlkopaoicige')
            message = MIMEText(tag + "\n" + content, 'plain', 'utf-8')
            message['From'] = self.sender  # Header("教程", 'utf-8')
            message['To'] = self.receivers[0]  # Header("接收者", 'utf-8')
            message['Subject'] = title
            # message['X-Mailer'] = Header('Microsoft Outlook Express 6.00.2900.2869', 'utf-8')
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print('发送成功')
            smtpObj.close()
            return True
        except smtplib.SMTPException as e:
            logger.info(e)
            return False

    def loop_call(self):
        keys = list(self.send_cache_list.keys())
        for key in keys:
            send_content = self.send_cache_list[key]
            while
                send_res = self.__send(send_content[0], key, send_content[1])
            # if send_res:
            #     del self.send_cache_list[key]
            time.sleep(2)
        pass


ee = ES()
for i in range(10):
    ee.append_send_list('内容' + str(i), 'tag')

ee.loop()
