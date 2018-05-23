import base64
import json
import os
import urllib

import django

# import imageio

# 设置django 环境
from Mryang_App.bats.ConvertBase import ConvertBase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir

# 设置解码环境
# imageio.plugins.ffmpeg.download()

from Mryang_App import yutils


class MediaConvert(ConvertBase):
    def __init__(self):
        super().__init__()

    def go(self):
        thum_root = '../../../static/media/pic'
        self.insert_dirs(yutils.M_FTYPE_MOIVE, thum_root, 'movie')

    def create_ffmpeg_bat(self):
        source_root = '../../../static/media/sourceFile/'
        target_root = '../../../static/media/targetFile/'
        bat_list = []
        for root, dirs, files in os.walk(source_root):
            for file in files:
                source_rela_path = os.path.join(root, file)

                # 创建文件夹
                # print(source_abs_path)
                file_name = source_rela_path[len(source_root):]
                target_dir = os.path.dirname(file_name)
                if target_dir:
                    encode = urllib.parse.quote(target_dir)
                    target_dir = target_root + encode
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        print('创建成功')
                    else:
                        print('已存在')
                else:
                    target_dir = target_root
                    print('无需创建')

                source_abs_path = os.path.abspath(source_rela_path)
                source_abs_path = source_abs_path.replace('\\', '/')
                (shotname, _) = os.path.splitext(file_name)
                target_abs_path = os.path.abspath(target_dir) + '\\' + os.path.basename(shotname) + '.mp4'
                target_abs_path = target_abs_path.replace('\\', '/')
                if not os.path.exists(target_abs_path):
                    bat_list.append('./ffmpeg/bin/ffmpeg -i %s %s' % (source_abs_path, target_abs_path))
                    print('source_abs_path:%s ,target_abs_path:%s' % (source_abs_path, target_abs_path))
                    # subprocess.call('ffmpeg -i %s %s' % (source_abs_path, target_abs_path))
                else:
                    print('已存在.')
                    # os.popen3('ffmpeg.exe -i %s %s' %s (source_abs_path,))

                    # target_abs_path =
                    # print("%s,隶属于 %s " % (nginx_path, os.path.dirname(nginx_path)))

                    # 需要获取文件绝对路径, source+

                    # 再需要获取输出路径.
        return bat_list

    def convert_media(self):
        bat_list = self.create_ffmpeg_bat()
        index = 0
        for i in bat_list:
            file_ = "./bats/%s.bat" % index
            if os.path.exists(file_):
                os.remove(file_)
            fp = open(file_, 'w')
            fp.write(i)
            fp.close()

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

    # def init_dirtype(self):
    #     pass


# 插入数据库
MediaConvert().go()

# 生成bat文件
# convert_media()

#     index += 1
# 负责生成bat文件.
# print('start')
# subprocess.call(
#     'ffmpeg -i F:/pywork/MrYangServer/static/media/sourceFile/源/英雄时刻_20171028-10点01分58s.avi F:/pywork/MrYangServer/static/media/targetFile/asdfwer/英雄时刻.mp4')
# print('success')
# os.popen3('ffmpeg.exe -i F:/static/media/video/1080.avi  F:/static/media/ffvideo/1080.mov')
