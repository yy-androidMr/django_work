import base64
import json
import os
import urllib

import django

# import imageio

# 设置django 环境

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Movie, Dir

# 设置解码环境
# imageio.plugins.ffmpeg.download()

from Mryang_App import yutils


# def flushdata_from_depth(max_show_depth, media_root, movie_root, depth_root):
#     media_root = media_root.replace('\\', '/')
#     movie_root = movie_root.replace('\\', '/')
#     depth_root = depth_root.replace('\\', '/')
#
#     for root, dirs, files in os.walk(depth_root):
#         for file in files:
#             if file.startswith('.'):
#                 continue
#
#             rela_path = os.path.join(root, file)
#             rela_path = rela_path.replace('\\', '/')
#             nginx_path = rela_path[len(movie_root):]
#             file_path = rela_path[len(media_root):]
#             dir_path = os.path.dirname(rela_path[len(depth_root):])
#             # nginx_path = urllib.parse.quote(nginx_path)// 不加码.在html里面加
#             media = Movie()
#             # # 获取文件名
#             media.name = file
#             media.nginx_path = nginx_path
#             fsize = os.path.getsize(rela_path)
#             media.length = utils.sizeConvert(fsize)
#             media.time = ''
#             media.static_path = file_path
#
#             # 这里要组织深度. 如果有文件夹,则计算
#             if dir_path:
#                 media.dir = dir_path + '/'
#                 dirs = dir_path.split('/')
#                 if len(dirs) >= max_show_depth:
#                     media.depth = max_show_depth
#                     pass
#                 else:
#                     media.depth = len(dirs)
#                     pass
#             else:
#                 media.dir = ''
#                 media.depth = 0
#             media.save()
#             print('add media:%s, nginx_path:%s , file:%s, filepath:%s,dirname:%s,depth:%s' % (
#                 rela_path, media.nginx_path, media.name, media.static_path, media.dir, media.depth))
#
#
# def flushdata(media_root, movie_root):
#     media_root = media_root.replace('\\', '/')
#     movie_root = movie_root.replace('\\', '/')
#
#     for root, dirs, files in os.walk(movie_root):
#         for file in files:
#             rela_path = os.path.join(root, file)
#             rela_path = rela_path.replace('\\', '/')
#             nginx_path = rela_path[len(movie_root):]
#             file_path = rela_path[len(media_root):]
#             dir_path = os.path.dirname(rela_path[len(movie_root):])
#             # nginx_path = urllib.parse.quote(nginx_path)// 不加码.在html里面加
#             media = Movie()
#             # # 获取文件名
#             media.name = file
#             media.nginx_path = nginx_path
#             fsize = os.path.getsize(rela_path)
#             media.length = utils.sizeConvert(fsize)
#             media.time = ''
#             media.static_path = file_path
#
#             # 这里要组织深度. 如果有文件夹,则计算
#             if dir_path:
#                 media.dir = dir_path + '/'
#                 dirs = dir_path.split('/')
#                 media.depth = len(dirs)
#             else:
#                 media.dir = ''
#                 media.depth = 0
#             media.save()
#             print('add media:%s, nginx_path:%s , file:%s, filepath:%s,dirname:%s,depth:%s' % (
#                 rela_path, media.nginx_path, media.name, media.static_path, media.dir, media.depth))
#
#
# def find_folders():
#     Movie.objects.all().delete()
#     media_root = '../../../static/media/'
#     movie_root = os.path.join(media_root, 'movie/')
# flushdata_from_depth(int(max_show_depth), media_root, movie_root, os.path.join(movie_root, file + '/'))

# files = os.listdir(movie_root)
# for file in files:
#     max_show_depth = file.split('_')[1]
#     flushdata_from_depth(int(max_show_depth), media_root, movie_root, os.path.join(movie_root, file + '/'))


# encode_rela_path = rela_path.encode(encoding='UTF-8')
# encode_rela_path.endswith()
# encode_rela_path.endswith('.gif')
# print(rela_path.encode(encoding='gbk'))
# clip = VideoFileClip(rela_path.encode(encoding='gbk'))


# print(nginx_path + ' 文件大小:' + utils.sizeConvert(fsize) + ' 视频长度:' + utils.timeConvert(rela_path))

# file_time = self.timeConvert(clip.duration)
# urlencode = urllib.parse.quote(rela_path)
# print(urllib.parse.unquote(urlencode))
# if file.endswith('.mp4'):
#     nginx_path = rela_path[len(media_root) + 1:]
#     # nginx_path = urllib.parse.quote(nginx_path)// 不加码.在html里面加
#     media = Medias()
#     # # 获取文件名
#     media.showname = file
#
#     media.nginxPath = nginx_path
#
#     fsize = os.path.getsize(rela_path)
#     media.moveLength = utils.sizeConvert(fsize)
#     media.movetime = ''
#     media.save()
#     print('add media:%s' % rela_path)
#     # encode_rela_path = rela_path.encode(encoding='UTF-8')
#     # encode_rela_path.endswith()
#     # encode_rela_path.endswith('.gif')
#     # print(rela_path.encode(encoding='gbk'))
#     # clip = VideoFileClip(rela_path.encode(encoding='gbk'))
#
#
#     # print(nginx_path + ' 文件大小:' + utils.sizeConvert(fsize) + ' 视频长度:' + utils.timeConvert(rela_path))
#
#     # file_time = self.timeConvert(clip.duration)
#     # urlencode = urllib.parse.quote(rela_path)
#     # print(urllib.parse.unquote(urlencode))
# else:
#     print('不是媒体文件:%s' % rela_path)

def create_ffmpeg_bat():
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
                bat_list.append('ffmpeg -i %s %s' % (source_abs_path, target_abs_path))
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


def convert_media():
    bat_list = convert_media()
    index = 0
    for i in bat_list:
        file_ = "./bats/%s.bat" % index
        if os.path.exists(file_):
            os.remove(file_)
        fp = open(file_, 'w')
        fp.write(i)
        fp.close()


def flush_dirs(source_path, rel_path, is_dir, name, fileType):
    source_path = source_path.replace('\\', '/')
    d_model = Dir()
    d_model.name = name
    d_model.isdir = is_dir
    self_abs_path = os.path.realpath(source_path).replace('\\', '/')
    d_model.abs_path = self_abs_path + ('/' if not is_dir else '')
    d_model.rel_path = rel_path
    parent_abs_path = os.path.dirname(self_abs_path)
    d_model.type = fileType
    try:
        parent_dir = Dir.objects.get(abs_path=parent_abs_path)
        d_model.parent_dir = parent_dir
    except:
        pass
    d_model.save()


def create_dirs(media_root, depthName, fileType):
    movie_name = depthName + '/'
    movie_root = os.path.join(media_root, movie_name)
    flush_dirs(movie_root, movie_name, True, depthName, fileType)

    movie_root = movie_root.replace('\\', '/')
    for root, dirs, files in os.walk(movie_root):
        for dir in dirs:
            source_path = os.path.join(root, dir).replace('\\', '/') + '/'
            rel_path = source_path[len(movie_root):]
            flush_dirs(source_path, rel_path, True, dir, fileType)

        for file in files:
            source_path = os.path.join(root, file).replace('\\', '/')
            rel_path = source_path[len(movie_root):]
            flush_dirs(source_path, rel_path, False, file, fileType)


def instart_dirs():
    Dir.objects.all().delete()
    media_root = '../../../static/media/'
    create_dirs(media_root, 'movie', yutils.M_FTYPE_MOIVE)
    create_dirs(media_root, 'pic', yutils.M_FTYPE_PIC)
    pass


def init_dirtype():
    pass


if __name__ == '__main__':
    instart_dirs()
    # convert_media()

    #     index += 1
    # 负责生成bat文件.
    # print('start')
    # subprocess.call(
    #     'ffmpeg -i F:/pywork/MrYangServer/static/media/sourceFile/源/英雄时刻_20171028-10点01分58s.avi F:/pywork/MrYangServer/static/media/targetFile/asdfwer/英雄时刻.mp4')
    # print('success')
    # os.popen3('ffmpeg.exe -i F:/static/media/video/1080.avi  F:/static/media/ffvideo/1080.mov')
