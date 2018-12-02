import os
import pickle

import django

# 设置django 环境
from MediaTools.DBTools.ConvertBase import ConvertBase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir

from frames import yutils


class MediaConvert(ConvertBase):
    def __init__(self):
        super().__init__()

    def go(self):
        # pass
        self.insert_dirs(yutils.M_FTYPE_MOIVE, self.media_root, 'movie')

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        if not is_dir:  # 不是文件的要return
            return

        if yutils.M3U8_DIR_EXTEN in name:
            # 这里做文件组织.
            is_dir = False

            with open(abs_path + '/' + yutils.INFO_FILE, 'rb') as f:
                info = pickle.load(f)
                name = info[yutils.MOVIE_INFO_NAME]
                # print(pickle.load(f))  # 只能以二进制写入
            # name = name + '/' + yutils.M3U8_NAME
            abs_path = abs_path + '/' + yutils.M3U8_NAME
            source_path = abs_path.replace('\\', '/')
            self_abs_path = os.path.realpath(source_path).replace('\\', '/')
            rel_path = rel_path + '/' + yutils.M3U8_NAME
            parent_abs_path = os.path.dirname(os.path.dirname(self_abs_path))

            # 这里读取info文件内容.
        else:
            source_path = abs_path.replace('\\', '/')
            self_abs_path = os.path.realpath(source_path).replace('\\', '/')
            parent_abs_path = os.path.dirname(self_abs_path)
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
    MediaConvert().go()

# with open(r'G:\pyWorkspace\django_work\MrYangServer\static\media\movie\d5e3f566488ffd2c59d394808ab9325b\info',
#           'rb') as f:
#     print(pickle.load(f))  # 只能以二进制写入
