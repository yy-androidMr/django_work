import threading
from time import ctime, sleep

from qq_login.MulThreadDownload import DownloadMe


def music(func):
    for i in range(2):
        print('method1  %s. %s , %s' % (func, ctime(), i))
        sleep(10)
        print('method1 finish  %s. %s' % (func, ctime()))


def move(func):
    for i in range(2):
        print('method2  %s. %s, %s' % (func, ctime(), i))
        # sleep(5)
        print('method2 finish  %s. %s' % (func, ctime()))


def start_download_http(args):
    print('start new download: %s' % args)
    DownloadMe(args).download()


threads = []


def start_download(url):
    if url.startswith('http'):
        # unicode('ftp://ygdy8:ygdy8@yg72.dydytt.net:6018/[阳光电影www.ygdy8.net].正yi联盟.HD.720p.韩版中英双字幕.rmvb', "utf-8")
        newdownload = threading.Thread(target=start_download_http, args=(url,))
        threads.append(newdownload)
        newdownload.name = url.split('/')[-1]
        newdownload.start()


# def ftpconnect(host, username, password):
#     ftp = FTP()
#     # ftp.set_debuglevel(2)
#     ftp.connect(host, 8234)
#     ftp.login(username, password)
#     return ftp
#
# def downloadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'wb')
#     ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()

if __name__ == '__main__':
    # ftp: // ygdy8: ygdy8 @ yg90.dydytt.net:8234 / [阳光电影www.ygdy8.net].小丑回魂.BD.720p.中英双字幕.mkv
    # start_download('https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi')
    # start_download('https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi')
    start_download('http://sw.bos.baidu.com/sw-search-sp/software/689272248105b/FlashFXP54_5.4.0.3970_Setup.exe')
    # start_download('ftp://ygdy8:ygdy8@yg90.dydytt.net:8234/[阳光电影www.ygdy8.net].小丑回魂.BD.720p.中英双字幕.mkv')
    # ftp = ftpconnect("yg90.dydytt.net", "ygdy8", "ygdy8")
    # downloadfile(ftp, "[阳光电影www.ygdy8.net].小丑回魂.BD.720p.中英双字幕.mkv", "C:/Users/Administrator/Desktop/test.mkv")


