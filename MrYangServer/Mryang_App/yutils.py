# coding:utf-8
import os
import random
import string
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
from Mryang_App.models import User


def random_int():
    return random.randint(10000000, 99999999)


def random_str():
    # random_str = []
    # for i in range(100):
    #     random_str.append(random.choice(seed))
    # return ''.join(random_str)
    # fun2:
    salt = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(8, 20)))
    return salt


def random_account():
    return random.choice(User.objects.all())


LOGIN_TIME_OUT = 7 * 24 * 60 * 60  # 7天失效

S_ACCOUNT = 'user_account'

S_NAME = 'user_name'

# media的文件类型.
M_FTYPE_MOIVE = 1
M_FTYPE_PIC = 2
M_FTYPE_DOC = 3


# end


def is_login(session):
    user_name = session.get(S_NAME, '')
    if user_name:
        return True
    else:
        return False


def get_s_account(session):
    act = session.get(S_ACCOUNT, '')
    return act


def logout(session):
    user_name = session.get(S_NAME)
    if user_name:
        del session[S_NAME]


def is_login_c(cookie):
    user_name = cookie.get(S_NAME, '')
    if user_name:
        return True
    else:
        return False


def get_s_account_c(cookie):
    act = cookie.get(S_ACCOUNT, '')
    return act


def download_file():
    a = ''
    # win32api.ShellExecute(0, 'open', 'D:\迅雷\Program\Thunder.exe', '', '', 1)
    # , unicode('ftp://ygdy8:ygdy8@yg72.dydytt.net:6018/[阳光电影www.ygdy8.net].正yi联盟.HD.720p.韩版中英双字幕.rmvb', "utf-8")
    # thunder: // QUFmdHA6Ly9nOmdAdHYua2FpZGEzNjUuY29tOjMxMDAvJUU1JUE0JUE3JUU1JTg2JTlCJUU1JUI4JTg4JUU1JThGJUI4JUU5JUE5JUFDJUU2JTg3JUJGJUU0JUI5JThCJUU4JTk5JThFJUU1JTk1JUI4JUU5JUJFJTk5JUU1JTkwJTlGMDUubXA0Wlo =
    # MulThreadDownload.download(unicode('ftp://ygdy8:ygdy8@yg72.dydytt.net:6018/[阳光电影www.ygdy8.net].正yi联盟.HD.720p.韩版中英双字幕.rmvb', "utf-8"))
    # url ="https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi"
    # local = os.path.join('static/download', 'cui.zip')
    # urllib.urlretrieve(url, local, print_download_prog)


def print_download_prog(downloaded, bytelist, totalbyte):
    per = 100.0 * downloaded * bytelist / totalbyte
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def sizeConvert(size):  # 单位换算
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        return str(round(size / G, 1)) + 'GB'
    elif size >= M:
        return str(round(size / M, 1)) + 'MB'
    elif size >= K:
        return str(round(size / K, 1)) + 'KB'
    else:
        return str(round(size, 1)) + 'Bytes'


def timeConvert(size):  # 单位换算
    M, H = 60, 60 ** 2
    if size < M:
        return str(size) + u'秒'
    if size < H:
        return u'%s分钟%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
        return tim_srt
