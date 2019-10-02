import ctypes
import os
import platform
import shutil
import sys
import time

import django

import manage
from Mryang_App import DBHelper
from frames import ypath, yutils

sys.path.append('./../../')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()
res_linkdir = (manage.root() / '../res_link').resolve()
from MryangService import ServiceHelper

from Mryang_App.models import MPath

sotrage_min = 8 * 1024 + 2 * 1024  # 最小空间有这么大G


class MPathDbCache:
    def __init__(self):
        self.src_list = []
        self.desc_list = []
        self.src_id_key = {}
        self.desc_id_key = {}
        self.src_abs_path_key = {}
        self.desc_abs_path_key = {}

    # def mpath_dict(type=None, byid=True):
    #     if type:
    #         mpath_query = MPath.objects.filter(type=type)
    #     else:
    #         mpath_query = MPath.objects.all()
    #     mpath_cache = {}
    #     for mpath_db in mpath_query:
    #         if byid:
    #             mpath_cache[mpath_db.id] = mpath_db.dir.abs_path
    #         else:
    #             mpath_cache[mpath_db.dir.abs_path] = mpath_db
    #
    #     return mpath_cache

    def reset(self):
        self.src_list.clear()
        self.desc_list.clear()

    def append(self, query):
        if query.type == 1:
            self.src_list.append(PathInfo(query))
            self.src_id_key[query.id] = query.dir.abs_path
            self.src_abs_path_key[self.src_id_key[query.id]] = query
            self.link(self.src_id_key[query.id], query.param1)
        elif query.type == 2:
            self.desc_list.append(PathInfo(query))
            self.desc_id_key[query.id] = query.dir.abs_path
            self.desc_abs_path_key[self.desc_id_key[query.id]] = query
            self.link(self.desc_id_key[query.id], query.param1, False)

    def link(self, abs_path, folder, isSrc=True):
        if isSrc:
            link = res_linkdir / 'msrc' / folder
        else:
            link = res_linkdir / 'mdesc' / folder
        if link.exists():
            os.remove(link)
        os.symlink(abs_path, link)

    def init_finish(self):
        if len(self.src_list) == 0:
            src()
        src()

        if len(self.desc_list) == 0:
            desc()
        self.src_list.sort(key=lambda x: x.level, reverse=True)
        self.desc_list.sort(key=lambda x: x.level, reverse=True)


mpath_db_cache = MPathDbCache()


class PathInfo:
    def __init__(self, query):
        self.query = query
        # if platform.system() == 'Windows':
        #     folder = folder.split('\\')[0].split('/')[0]
        # else:
        # self.dir_abs_path = self.query.dir.abs_path
        self.cur_memo = 0
        self.update_mem()

    @property
    def path(self):
        return self.query.dir.abs_path

    @property
    def level(self):
        return self.query.level

    def can_use(self):
        return self.query.drive_memory_mb < self.cur_memo

    # 耗时操作. 需要斟酌:10万次4秒
    def update_mem(self):
        self.cur_memo = self.get_free_storage_mb(self.query.dir.abs_path)

    @staticmethod
    def get_free_storage_mb(folder):
        folder = folder.split('\\')[0].split('/')[0]
        return shutil.disk_usage(folder)[2] // 1024 // 1024


def need_input(intro, storage_low='所选磁盘剩余容量过小,请重新选择\n', path_exist='目标目录已存在!请重新选择:\n'):
    path_str = None
    # 是文件夹.并且磁盘的空间需要大于
    while True:
        if path_str is None or not os.path.exists(path_str):
            path_str = input(intro)
        elif sotrage_min > PathInfo.get_free_storage_mb(path_str):
            path_str = input(storage_low)
        else:
            path_str = ypath.convert_path(path_str)
            if MPath.objects.filter(dir__abs_path=path_str).count() > 0:
                path_str = input(path_exist)
            else:
                break
    return ypath.convert_path(path_str)


def insert_path(path, type):
    query_ress = MPath.objects.filter(dir__abs_path=path)
    if query_ress.count() == 0:
        dir = ServiceHelper.create_dir_root(path, yutils.M_FTYPE_MPATH)
        mpath = MPath()
        # mpath.path = path
        mpath.type = type
        mpath.param1 = yutils.md5_of_str(path)
        mpath.dir = dir
        mpath.save()
        return mpath
    else:
        print('不可以了. 数据库有字段了')
        assert query_ress[0].type == type
        return query_ress[0]


def get_path(path_info_list, type, intro):
    for path_item in path_info_list:
        path_item.update_mem()
        if path_item.can_use():
            return path_item.query.dir.abs_path
    path = need_input(intro)
    query_res = insert_path(path, type)
    mpath_db_cache.append(query_res)
    return query_res.dir.abs_path


# 添加可以. 修改删除不行. 正在同步时
def src():
    return get_path(mpath_db_cache.src_list, DBHelper.MPathHelp.SRC,
                    'src目录对应的磁盘已满,或src目录不正确.请重新输入磁盘目录(目录下有pic文件夹,media文件夹):\n')


def desc():
    return get_path(mpath_db_cache.desc_list, DBHelper.MPathHelp.DESC,
                    'desc目录对应的磁盘已满,或desc目录不正确.请重新输入磁盘目录(目录下会创建pic文件夹,media文件夹):\n')


def init():
    mpath_db_cache.reset()
    # download_list.clear()
    query_res = MPath.objects.all()
    for query in list(query_res):
        mpath_db_cache.append(query)
    # 没有设置.需要设置!
    mpath_db_cache.init_finish()


init()
