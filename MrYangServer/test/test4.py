# import subprocess
# out =subprocess.check_output('ping www.baidu.com',shell=True)
# print(out.decode('gbk'))
# print(decode('utf-8'))
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP

from frames import ypath, yutils

# ypath.delrepeat_file(r'F:\cache\照片导出')

smtpObj = None
sender = '1702497572@qq.com'
receivers = ['1226341090@qq.com']
try:
    smtpObj = smtplib.SMTP_SSL(host='smtp.qq.com')
    smtpObj.connect(host='smtp.qq.com', port=465)
    smtpObj.login(sender, 'qjmrhlkopaoicige')
    # message = MIMEText('我的啊的~ 撒旦哈哈哈22', 'plain', 'utf-8')
    # message['From'] = sender  # Header("教程", 'utf-8')
    # message['To'] = receivers[0]  # Header("接收者", 'utf-8')
    # # message['X-Mailer'] = Header('Microsoft Outlook Express 6.00.2900.2869', 'utf-8')
    # smtpObj.sendmail(sender, receivers, message.as_string())
    # print('发送成功')
except smtplib.SMTPException as e:
    print(e)

# for i in range(5):
try:
    message = MIMEText('我的啊的~ 撒旦哈哈哈', 'plain', 'utf-8')
    message['From'] = sender  # Header("教程", 'utf-8')
    message['To'] = receivers[0]  # Header("接收者", 'utf-8')
    message['Subject'] = '来自SMTP的问候...'
    # message['X-Mailer'] = Header('Microsoft Outlook Express 6.00.2900.2869', 'utf-8')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print('发送成功')
except smtplib.SMTPException as e:
    print(e)
# time.sleep(10)
