import smtplib
import threading
from email.mime.text import MIMEText

sending = False
lock = threading.Lock()
MAX_TAG_CACHE_COUNT = 10  # 每一个tag的最多数量.
send_cache_list = {}


def append_send_list(content, tag, title='01-pc的通知'):
    if tag not in send_cache_list:
        send_cache_list[tag] = []
        pass
    tag_list = send_cache_list.get(tag)
    if len(tag_list) > MAX_TAG_CACHE_COUNT:
        del tag_list[0]
    tag_list.append((title, content))


smtpObj = None
sender = '1702497572@qq.com'
receivers = ['1226341090@qq.com']


def send(content, title='01-pc的通知'):
    global sending
    with lock:
        if sending:
            print('正在发送. ')
            return
        try:
            sending = True
            smtpObj = smtplib.SMTP_SSL(host='smtp.qq.com')
            smtpObj.connect(host='smtp.qq.com', port=465)
            smtpObj.login(sender, 'qjmrhlkopaoicige')
            message = MIMEText(content, 'plain', 'utf-8')
            message['From'] = sender  # Header("教程", 'utf-8')
            message['To'] = receivers[0]  # Header("接收者", 'utf-8')
            message['Subject'] = title
            # message['X-Mailer'] = Header('Microsoft Outlook Express 6.00.2900.2869', 'utf-8')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print('发送成功')
            smtpObj.close()
            sending = False
        except smtplib.SMTPException as e:
            print(e)
