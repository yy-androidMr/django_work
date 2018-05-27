import os
import pickle

import django

# 设置django 环境
from Mryang_App.bats.ConvertBase import ConvertBase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir

from Mryang_App import yutils


class MediaConvert(ConvertBase):
    def __init__(self):
        super().__init__()

    def go(self):
        thum_root = '../../../static/media/pic'
        self.insert_dirs(yutils.M_FTYPE_MOIVE, thum_root, 'movie')

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        source_path = abs_path.replace('\\', '/')
        d_model = Dir()
        d_model.name = name
        d_model.isdir = is_dir
        self_abs_path = os.path.realpath(source_path).replace('\\', '/')
        d_model.abs_path = self_abs_path + ('/' if not is_dir else '')
        d_model.rel_path = rel_path
        parent_abs_path = os.path.dirname(self_abs_path)
        d_model.type = yutils.M_FTYPE_MOIVE
        try:
            parent_dir = Dir.objects.get(abs_path=parent_abs_path)
            d_model.parent_dir = parent_dir
        except:
            pass
        d_model.save()


# 插入数据库
# MediaConvert().go()

# path = ''.join(['../../../static/media/movie/09f5bc8ebc65e1efbcd9105adf052da7', '/info'])
# print(os.path.abspath(path))
# pickle_file = open(path, 'wb+')
# print(pickle_file.readlines())
# sss = pickle.load(pickle_file)
# pickle_file.close()
# print(sss)