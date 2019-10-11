import base64
import email
import poplib
import smtplib
import time
from email.mime.text import MIMEText
from email.parser import Parser

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
            smtpObj.quit()
            smtpObj.close()
            return True
        except smtplib.SMTPException as e:
            logger.info(e)
            return False

    def loop_call(self):
        keys = list(self.send_cache_list.keys())
        for key in keys:
            tag_list = self.send_cache_list[key]
            while len(tag_list) > 0:
                send_tupe = tag_list[0]
                print(send_tupe)
                send_res = self.__send(send_tupe[1], key, send_tupe[0])
                if send_res:
                    del tag_list[0]
                    time.sleep(2)
                else:
                    break


def receive():
    server = poplib.POP3('pop.qq.com')
    # server.set_debuglevel(1)
    server.user('1702497572@qq.com')
    server.pass_('qjmrhlkopaoicige')
    email_num, email_size = server.stat()
    print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))

    rsp, msg_list, rsp_siz = server.list()
    print("服务器的响应: {0},\n消息列表： {1}".format(rsp, msg_list))

    # print('邮件总数： {}'.format(len(msg_list)))

    # 下面单纯获取最新的一封邮件
    total_mail_numbers = len(msg_list)
    rsp, msglines, msgsiz = server.retr(total_mail_numbers)
    # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))
    msg_content = b'\r\n'.join(msglines).decode('gbk')
    msg = Parser().parsestr(text=msg_content)
    # print('解码后的邮件信息:\n{}'.format(msg))
    server.close()

    def parser_address(msg):
        hdr, addr = email.utils.parseaddr(msg['From'])
        # name 发送人邮箱名称， addr 发送人邮箱地址
        name, charset = email.header.decode_header(hdr)[0]
        if charset:
            name = name.decode(charset)
        print('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr))

    def parser_content(msg):
        content = msg.get_payload()

        # 文本信息
        content_charset = content[0].get_content_charset()  # 获取编码格式
        text = content[0].as_string().split('base64')[-1]
        text_content = base64.b64decode(text).decode(content_charset)  # base64解码

        # 添加了HTML代码的信息
        content_charset = content[1].get_content_charset()
        text = content[1].as_string().split('base64')[-1]
        html_content = base64.b64decode(text).decode(content_charset)
        print('文本信息:::' + str(text_content))
        # print('文本信息: {0}\n添加了HTML代码的信息: {1}'.format(text_content, html_content))

    def parser_subject(msg):
        subject = msg['Subject']
        value, charset = email.header.decode_header(subject)[0]
        if charset:
            value = value.decode(charset)
        print('邮件主题： {0}'.format(value))
        return value

    print("发送时间:" + str(email.utils.parsedate(msg['Date'])))
    parser_address(msg)
    # parser_subject(msg)
    parser_content(msg)


while True:
    receive()
    time.sleep(2)
