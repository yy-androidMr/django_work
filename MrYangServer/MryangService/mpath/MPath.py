import ctypes
import os
import platform
import sys
import time

import django

sys.path.append('./../../')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()
from Mryang_App.models import MPath

sotrage_min = 8 * 1024 + 2 * 1024  # 最小空间有这么大G
src_list = []
desc_list = []


class PathInfo:
    def __init__(self, query):
        self.query = query
        self.cur_memo = 0
        self.update_mem()

    @property
    def path(self):
        return self.query.path

    @property
    def level(self):
        return self.query.level

    def can_use(self):
        return self.query.drive_memory_mb < self.cur_memo

    def update_mem(self):
        self.cur_memo = self.get_free_storage_mb(self.query.path)

    @staticmethod
    def get_free_storage_mb(folder):
        if platform.system() == 'Windows':
            folder = folder.split('\\')[0].split('/')[0]
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value / 1024 // 1024
        else:
            st = os.statvfs(folder)
            return st.f_bavail * st.f_frsize // 1024


def init():
    src_list.clear()
    desc_list.clear()
    # download_list.clear()
    query_res = MPath.objects.all()
    for query in list(query_res):
        if query.type == 1:
            src_list.append(PathInfo(query))
        elif query.type == 2:
            desc_list.append(PathInfo(query))
        # elif query.type == 3:
        #     download_list.append(path_info(query))
        # elif query.type == 4:
        #     upload_list.append(path_info(query))
    src_list.sort(key=lambda x: x.level, reverse=True)
    desc_list.sort(key=lambda x: x.level, reverse=True)


init()


def need_input(intro, storage_low='所选磁盘剩余容量过小,请重新选择\n', path_exist='目标目录已存在!请重新选择:\n'):
    path_str = None
    # 是文件夹.并且磁盘的空间需要大于
    while True:
        if path_str is None or not os.path.exists(path_str):
            path_str = input(intro)
        elif sotrage_min > PathInfo.get_free_storage_mb(path_str):
            path_str = input(storage_low)
        else:
            path_str = convert_path(path_str)
            if MPath.objects.filter(path=path_str).count() > 0:
                path_str = input(path_exist)
            else:
                break
    return convert_path(path_str)


# 统一处理一下path
def convert_path(path):
    path = path.replace('\\', '/').replace('//', '/')
    if path.endswith('/'):
        return path[:-1]
    return path


def insert_path(path, type):
    query_ress = MPath.objects.filter(path=path)
    if query_ress.count() == 0:
        mpath = MPath()
        mpath.path = path
        mpath.type = type
        mpath.save()
        return mpath
    else:
        print('不可以了. 数据库有字段了')
        assert query_ress[0].type == type
        return query_ress[0]


def get_path(path_info_list, type, intro):
    for path_item in path_info_list:
        if path_item.can_use():
            return path_item.query.path
    path = need_input(intro)
    query_res = insert_path(path, type)
    path_info_list.append(PathInfo(query_res))
    return query_res.path


# 添加可以. 修改删除不行. 正在同步时
def src():
    return get_path(src_list, 1, 'src目录对应的磁盘已满,或src目录不正确.请重新输入磁盘目录(目录下有pic文件夹,media文件夹):\n')


def desc():
    return get_path(desc_list, 2, 'desc目录对应的磁盘已满,或desc目录不正确.请重新输入磁盘目录(目录下会创建pic文件夹,media文件夹):\n')
