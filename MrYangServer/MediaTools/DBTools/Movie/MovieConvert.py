import glob
import os
import pickle

import django

# 设置django 环境
from MediaTools.DBTools.ConvertBase import ConvertBase
from Mryang_App.models import Dir
from frames.xml import XMLMovie, XMLBase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()

from frames import yutils

movie_config = XMLMovie.get_infos()


class MovieConvert(ConvertBase):
    def __init__(self):
        super().__init__()

    def go(self):
        res_root, _ = XMLBase.resource_root()
        self.insert_dirs(yutils.M_FTYPE_MOIVE, res_root, movie_config[XMLMovie.TAGS.DIR_ROOT])

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        if not is_dir:  # 不是文件的要return
            return

        if movie_config[XMLMovie.TAGS.DIR_EXTEN] in name:
            # 这里做文件组织.
            is_dir = False

            # name = movie_info.name
            # print(pickle.load(f))  # 只能以二进制写入
            # name = name + '/' + yutils.M3U8_NAME
            abs_path = abs_path + '/' + movie_config[XMLMovie.TAGS.NAME]
            source_path = abs_path.replace('\\', '/')
            self_abs_path = os.path.realpath(source_path).replace('\\', '/')
            rel_path = rel_path + '/' + movie_config[XMLMovie.TAGS.NAME]
            parent_abs_path = os.path.dirname(os.path.dirname(self_abs_path))

            # 这里读取info文件内容.
        else:
            source_path = abs_path.replace('\\', '/')
            self_abs_path = os.path.realpath(source_path).replace('\\', '/')
            parent_abs_path = os.path.dirname(self_abs_path)

        print(abs_path, source_path, self_abs_path, rel_path, parent_abs_path, sep='][')
        # pass
        d_model = Dir()
        d_model.name = name
        d_model.isdir = is_dir
        d_model.abs_path = self_abs_path
        d_model.rel_path = rel_path
        d_model.type = yutils.M_FTYPE_MOIVE
        try:
            parent_dir = Dir.objects.get(abs_path=parent_abs_path)
            d_model.parent_dir = parent_dir
        except:
            pass
        d_model.save()

# 插入数据库
if __name__ == '__main__':
    # info_dict = XMLMovie.item_info_dict()
    # MovieConvert().go()
    res_root, _ = XMLBase.resource_root()
    listglob = glob.glob(r'G:\pyWorkspace\django_work\MrYangServer\static\res\movie\*\*.ym3')
    print(listglob)

# with open(r'G:\pyWorkspace\django_work\MrYangServer\static\media\movie\d5e3f566488ffd2c59d394808ab9325b\info',
#           'rb') as f:
#     print(pickle.load(f))  # 只能以二进制写入
