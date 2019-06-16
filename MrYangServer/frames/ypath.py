# coding:utf-8


import os
import re
import shutil
from pathlib import PurePath

from frames import yutils


class KEYS:
    LEVEL = 'level'
    NAME = 'name'
    IS_DIR = 'is_dir'
    REL = 'rel_path'
    PARENT = 'parent_path'


def parse_path(path, root_path, name, isDir=False):
    parent_path = os.path.dirname(path)
    rel_path = path[len(root_path):]

    return {KEYS.LEVEL: rel_path.count('/'), KEYS.NAME: name, KEYS.IS_DIR: isDir, KEYS.REL: rel_path,
            KEYS.PARENT: parent_path}


# def path_res(root, dir_filter=None, file_filter=None, parse_dir=True, parse_file=True, add_root=True):
#     dict = {}
#     if add_root:
#         dict[root] = parse_path(root, root, root.name, True)
#     for root, dirs, files in os.walk(root):
#         if parse_dir:
#             for dir in dirs:
#                 source_path = join(root, dir)
#                 if dir_filter:
#                     if re.match(dir_filter, source_path):
#                         dict[source_path] = parse_path(source_path, root_path, dir, True)
#                 else:
#                     dict[source_path] = parse_path(source_path, root_path, dir, True)
#         if parse_file:
#             for file in files:
#                 if '.DS_Store' in file:
#                     continue
#                 source_path = join(root, file)
#                 if file_filter:
#                     if re.match(file_filter, source_path):
#                         dict[source_path] = parse_path(source_path, root_path, file)
#                 else:
#                     dict[source_path] = parse_path(source_path, root_path, file)
#     return dict

# 获取所有文件和文件夹
def list_folder(path, include_file=True, include_dir=True):
    path = replace(str(path))
    res = []
    if include_dir:
        res.append(path)
    for root, dirs, files in os.walk(path):
        if include_file:
            res.extend([join(root, file) for file in files])
        if include_dir:
            res.extend([join(root, dir) for dir in dirs])
    return res


# 获取所有文件的相对路径
def releative_list(path):
    m_path = replace(str(path))
    res = []
    for root, dirs, files in os.walk(m_path):
        res.extend([join(root, file).replace(m_path, '') for file in files])
        res.extend([join(root, dir).replace(m_path, '') for dir in dirs])
    return res


class PathClass:
    def __init__(self, path, root):
        s_root = replace(str(root))
        self.path = replace(str(path))
        if self.path.endswith('/'):
            self.path = self.path[:-1]
        self.is_dir = os.path.isdir(self.path)  # path.is_dir()
        self.name = os.path.basename(self.path)  # path.name
        self.relative = '.' if s_root == self.path else self.path[len(s_root):]
        self.level = self.relative.count('/')
        self.parent = os.path.dirname(self.path)  # str(path.parent.as_posix())

    def __eq__(self, other):
        return other == self.path

    def __str__(self):
        return '%s,is_dir:%s,name:%s,relative:%s,level:%s,parent:%s' % (
            self.path, self.is_dir, self.name, self.relative, self.level, self.parent)


def path_res(path, parse_dir=True, parse_file=True):
    m_file_list = []
    files = list_folder(path)  # path.rglob('*')
    for file in files:
        cache_it = False
        if parse_dir and os.path.isdir(file):  # .is_dir():
            cache_it = True
        elif parse_file and os.path.isfile(file):  # is_file():
            cache_it = True
        if cache_it:
            res = PathClass(file, path)
            m_file_list.append(res)
    return m_file_list


# 获取res_root文件夹下的的所有文件夹和文件名.
def path_result(res_root, depth_name, dir_filter=None, file_filter=None, parse_dir=True, parse_file=True,
                add_root=True):
    root_path = join(res_root, depth_name)
    dict = {}
    if add_root:
        dict[root_path] = parse_path(root_path, root_path, depth_name, True)
    for root, dirs, files in os.walk(root_path):
        if parse_dir:
            for dir in dirs:
                source_path = join(root, dir)
                if dir_filter:
                    if re.match(dir_filter, source_path):
                        dict[source_path] = parse_path(source_path, root_path, dir, True)
                else:
                    dict[source_path] = parse_path(source_path, root_path, dir, True)
        if parse_file:
            for file in files:
                if '.DS_Store' in file:
                    continue
                source_path = join(root, file)
                if file_filter:
                    if re.match(file_filter, source_path):
                        dict[source_path] = parse_path(source_path, root_path, file)
                else:
                    dict[source_path] = parse_path(source_path, root_path, file)
    return dict


def replace(str):
    return str.replace('\\', '/').replace('//', '/')


def decompose_path(src_file, src_root, target_root, exten=None, rename=None):
    # 需要返回几个值:
    # 1.去掉src_root的相对路径.
    src_file = replace(src_file)
    rela_file_name = src_file[len(src_root):]

    # 2.替换后缀或者替换名字
    if rename:
        rela_file_name = join(os.path.dirname(rela_file_name), rename)
    elif exten:
        rela_file_name = ''.join([del_exten(rela_file_name), exten])

    # 3.新的目标文件
    target_file = join(target_root, rela_file_name)

    return rela_file_name, target_file


# 返回不带io操作的path
def pp_ins(base_path):
    return PurePath(base_path)


def join(path, *paths):
    new_paths = []
    for item in paths:
        if item.startswith('/') or item.startswith('\\'):
            new_paths.append(item.lstrip('/').lstrip('\\'))
        else:
            new_paths.append(item)
    path = os.path.join(path, *tuple(new_paths)).replace('\\', '/').replace('//', '/')
    return path


def abspath(path):
    abs = os.path.abspath(path)
    return replace(abs)


def del_exten(path):
    if path:
        return os.path.splitext(path)[0]


def file_name(path):
    if path:
        return del_exten(os.path.basename(path))


# 拓展名.
def file_exten(file):
    return os.path.splitext(file)[1]


# 移动文件
def move_file(file, desc):
    if os.path.isfile(file):
        create_dirs(file, delete_exist=True)
        shutil.move(file, desc)


def compair_path(left, right):
    left = replace(left)
    right = replace(right)
    left_set = set([])
    for root, dirs, files in os.walk(left):
        for dir in dirs:
            left_set.add(join(root, dir).replace(left, ''))
        for file in files:
            left_set.add(join(root, file).replace(left, ''))

    right_set = set([])
    for root, dirs, files in os.walk(right):
        for dir in dirs:
            right_set.add(join(root, dir).replace(right, ''))
        for file in files:
            right_set.add(join(root, file).replace(right, ''))

    left_have = left_set.difference(right_set)
    right_have = right_set.difference(left_set)
    return left_have, right_have


# 删除所有文件中 有重复的图.
def delrepeat_file(path):
    print(path)
    repeat_file = {}
    for root, dirs, files in os.walk(path):
        md5_list = {}
        for file in files:
            source_rela_path = os.path.join(root, file)
            file_md5 = yutils.get_md5(source_rela_path)
            if file_md5 in md5_list:
                repeat_file[source_rela_path] = md5_list[file_md5]
            else:
                md5_list[file_md5] = os.path.abspath(source_rela_path)
        print('next')
    print(repeat_file)
    for file in repeat_file:
        print(file)
        os.remove(file)
    print('done')


def create_dirs(file_path, is_dir=False, delete_exist=False):
    if is_dir:
        target_dir = file_path
    else:
        target_dir = os.path.dirname(file_path)

    if target_dir:
        if os.path.exists(target_dir):
            if delete_exist:
                shutil.rmtree(target_dir)
            else:
                return
        os.makedirs(target_dir)


# 删除空文件夹
def del_none_dir(dir):
    if os.path.isdir(dir):
        for item in os.listdir(dir):
            del_none_dir(join(dir, item))

        if not os.listdir(dir):
            os.rmdir(dir)


def sync_role(path):
    return '.' + file_name(path) + '.tmp'

# 做文件处理的时候一个无奈锁.   如果有该文件锁,代表这个处理还未完成.
# def lock_path(path):
#     create_dirs(sync_role(path))
#
#
# def path_in_lock(path):
#     return os.path.exists(sync_role(path))
#
#
# def unlock_path(path):
#     lock_key = sync_role(path)
#     if os.path.exists(lock_key):
#         shutil.rmtree(lock_key)
# ------------------------------------------------------------------------
