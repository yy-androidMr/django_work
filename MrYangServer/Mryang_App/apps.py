from __future__ import unicode_literals

import threading
import time

from django.apps import AppConfig


# 初始化上传文件夹中的所有照片的md5值.
def init_upload_pic():
    time.sleep(1)
    pass

def init():
    t = threading.Thread(target=init_upload_pic)
    t.start()


class MryangAppConfig(AppConfig):
    name = 'Mryang_App'

    def ready(self):
        print('app ready')
        init()
        threads = threading.enumerate()
        for thread in threads:
            print(thread)
