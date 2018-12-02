# coding:utf-8

import sys, django, os
import threading
import time

import manage
# from Mryang_App.models import User
from frames.xml import XMLBase

proj_abs_path = os.path.abspath(os.path.join(sys.argv[0], '../..'))
sys.path.append(proj_abs_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()

# Create your tests here.
from frames.yutils import *

user_list = {'tk1': 'yy', 'tk2': 'wwjt', 'tk3': 'dd', 'tk4': '44ss', 'tk5': 'zzz', 'tk6': 'bb'}


class A():
    def __str__(self):
        return 'a'


# if __name__ == '__main__':
#     print(A())
#     main()
#     print('done!:')

import base64


def baseurl(url):
    if url.startswith('thunder://'):
        url = url[10:] + '\n'
        url = base64.decodestring(url)
        url = url[2:-2]
    elif url.startswith('flashget://'):
        url = url[11:url.find('&')] + '\n'
        url = base64.decodestring(url)
        url = url[10:-10]
    elif url.startswith('qqdl://'):
        url = url[7:] + '\n'
        url = base64.decodestring(url)
    else:
        print('\n It is not a available url!!')
    return url


# www.iplaypy.com

def test():
    url = 'thunder://QUFmdHA6Ly95Z2R5ODp5Z2R5OEB5ZzQ1LmR5ZHl0dC5uZXQ6NzA5Mi9bJUU5JTk4JUIzJUU1JTg1JTg5JUU3JTk0JUI1JUU1JUJEJUIxd3d3LnlnZHk4Lm5ldF0uJUU4JThCJUIxbHVuJUU1JUFGJUI5JUU1JTg2JUIzLkhELjcyMHAuJUU1JTlCJUJEJUU4JThCJUIxJUU1JThGJThDJUU4JUFGJUFELiVFNCVCOCVBRCVFOCU4QiVCMSVFNSU4RiU4QyVFNSVBRCU5NyVFNSVCOSU5NS5ta3ZaWg=='
    p = baseurl(url)
    print('\n============请将下面地址复制到你的下载器中=============\n')
    print(p)


def thread_run(arg):
    print('begin run it :' + str(arg))
    for i in range(0, 100):
        time.sleep(1)
        # print('run it :' + str(arg) + "  wait count:" + str(i) + "\n")


if __name__ == '__main__':
    # print(threading.currentThread())
    # for i in range(0, 4):
    #     t = threading.Thread(target=thread_run, args=(i,))
    #     t.name = '重新起县城名:' + str(i)
    #     t.start()
    #
    # threads = threading.enumerate()
    # for thread in threads:
    #     print(thread)
    # print(base64.b64encode('红楼梦小戏骨'))
    # print(manage.project_root())
    banner = XMLBase.get_gif_banner()
  #  banner = XMLBase.cfg_list_path('gallery_info')
    print(banner)
    pass
