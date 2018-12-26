# coding:utf-8


# 分解路径1.src的相对路径. 2.src的根目录. 3.目标的路径
import os
import re

import imageio

# 组织文件夹数据  dir_filter='^.+\\.ym3$'
# dict = {'/Users/mr.yang/Documents/GitHub/django_work/MrYangServer/static/res/movie/22sd/c213.ym3':
#         {'name': 'c213.ym3', 'isdir': True,'rel_path':'22sd/c213.ym3'
#          'parent':'/Users/mr.yang/Documents/GitHub/django_work/MrYangServer/static/res/movie/22sd' }}
from frames import logger


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


def path_result(res_root, depth_name, dir_filter=None, file_filter=None, parse_dir=True, parse_file=True,
                add_root=True):
    root_path = join(res_root, depth_name)
    logger.info('ypath:path_result:', res_root, root_path)
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

    return (rela_file_name, target_file)


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
    return (left_have, right_have)
    # ret_list = list( ^ )
    # ret2_list = list(set(right_files) ^ set(left_files))
    # print(ret_list)
    # print(ret2_list)


print(compair_path(r'G:\cache\11\pic\middle', r'G:\cache\11\pic\thum'))
