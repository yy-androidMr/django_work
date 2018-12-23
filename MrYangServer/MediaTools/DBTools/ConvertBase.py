# coding=utf-8
import os
import re

import django

from frames import yutils, TmpUtil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir


class KEYS:
    NAME = 'name'
    IS_DIR = 'is_dir'
    REL = 'rel_path'
    PARENT = 'parent_path'


def parse_path(path, root_path, name, isDir=False):
    path = path.replace('\\', '/')
    parent_path = os.path.dirname(path)
    rel_path = path[len(root_path):]

    return {KEYS.NAME: name, KEYS.IS_DIR: isDir, KEYS.REL: rel_path, KEYS.PARENT: parent_path}


# 组织文件夹数据  dir_filter='^.+\\.ym3$'
# dict = {'/Users/mr.yang/Documents/GitHub/django_work/MrYangServer/static/res/movie/22sd/c213.ym3':
#         {'name': 'c213.ym3', 'isdir': True,'rel_path':'22sd/c213.ym3'
#          'parent':'/Users/mr.yang/Documents/GitHub/django_work/MrYangServer/static/res/movie/22sd' }}
def path_result(c_type, res_root, depth_name, dir_filter=None, file_filter=None, parse_dir=True, parse_file=True):
    Dir.objects.filter(type=c_type).delete()
    root_path = os.path.join(res_root, depth_name)
    print(res_root, root_path)
    dict = {}
    dict[root_path] = parse_path(root_path, root_path, depth_name, True)
    for root, dirs, files in os.walk(root_path):
        if parse_dir:
            for dir in dirs:
                source_path = os.path.join(root, dir).replace('\\', '/')
                # rel_path = source_path[len(movie_root):]
                # self.flush_dirs(source_path, rel_path, True, dir, type)
                if dir_filter:
                    if re.match(dir_filter, source_path):
                        dict[source_path] = parse_path(source_path, root_path, dir, True)
                else:
                    dict[source_path] = parse_path(source_path, root_path, dir, True)
        if parse_file:
            for file in files:
                if '.DS_Store' in file:
                    continue
                source_path = os.path.join(root, file).replace('\\', '/')
                dict[source_path] = parse_path(source_path)
                if file_filter:
                    if re.match(file_filter, source_path):
                        dict[source_path] = parse_path(source_path, root_path, file)
                else:
                    dict[source_path] = parse_path(source_path, root_path, file)

        # rel_path = source_path[len(movie_root):]
        # self.flush_dirs(source_path, rel_path, False, file, type)

    print(dict)


class ConvertBase:
    def __init__(self):
        self.res_desc_root = TmpUtil.get(yutils.RESOURCE_DESC_KEY)

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        pass

    def walk_over(self):
        pass

    def flush_dirs(self, source_path, rel_path, is_dir, name, type):
        source_path = source_path.replace('\\', '/')
        self_abs_path = os.path.realpath(source_path).replace('\\', '/')
        parent_abs_path = os.path.dirname(self_abs_path)
        parent = None
        try:
            parent = Dir.objects.get(abs_path=parent_abs_path)
        except Exception as e:
            print('错误:%s:is not found :%s' % (parent_abs_path, e))
            pass

        self.walk_call(self_abs_path, rel_path, parent, name, is_dir)

    def create_dirs(self, media_root, depth_name, type):
        movie_name = depth_name
        movie_root = os.path.join(media_root, movie_name)
        self.flush_dirs(movie_root, movie_name, True, depth_name, type)

        movie_root = movie_root.replace('\\', '/')
        for root, dirs, files in os.walk(movie_root):
            for dir in dirs:
                source_path = os.path.join(root, dir).replace('\\', '/')
                rel_path = source_path[len(movie_root):]
                self.flush_dirs(source_path, rel_path, True, dir, type)

            for file in files:
                source_path = os.path.join(root, file).replace('\\', '/')
                rel_path = source_path[len(movie_root):]
                self.flush_dirs(source_path, rel_path, False, file, type)

    def insert_dirs(self, c_type, root, depth_name):
        Dir.objects.filter(type=c_type).delete()
        self.create_dirs(root, depth_name, c_type)
        self.walk_over()
        pass
