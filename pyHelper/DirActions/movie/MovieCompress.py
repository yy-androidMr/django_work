import json
import os
import urllib

import imageio
import numpy
import pylab
import skvideo.io
import skvideo.datasets

import yy_utils

source_root = yy_utils.media_source + '/movie'
target_root = yy_utils.media_source + '/movie_bat'


def is_movie(path):
    if not any(str_ in path for str_ in ('.mp4', '.mkv', '.rmvb', '.avi')):
        return False
    return True


def create_ffmpeg_bat():
    bat_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            source_rela_path = os.path.join(root, file)

            if not is_movie(file):
                continue
            file_name = source_rela_path[len(source_root):]
            # target_dir = os.path.dirname(file_name)
            source_abs_path = os.path.abspath(source_rela_path)
            target_abs_path = os.path.abspath(target_root) + '\\' + file_name + '.mp4'
            target_abs_path = target_abs_path.replace('\\', '/').replace('//', '/')

            # if target_dir:
            #     print(target_dir)
            #     target_dir = target_root + '/bat'
            #     if not os.path.exists(target_dir):
            #         os.makedirs(target_dir)
            #         print('创建成功')
            #     else:
            #         print('已存在')
            # else:
            #     target_dir = target_root
            #     print('无需创建')

            # source_abs_path = os.path.abspath(source_rela_path)
            # (shotname, _) = os.path.splitext(file_name)
            # target_abs_path = os.path.abspath(target_dir) + '\\' + os.path.basename(shotname) + '.mp4'
            # target_abs_path = target_abs_path.replace('\\', '/')
            yy_utils.create_dirs(target_abs_path)

            # if not os.path.exists(target_abs_path):
            bat_list.append('./ffmpeg/bin/ffmpeg -i %s %s' % (source_abs_path, target_abs_path))
            # print('source_abs_path:%s ,target_abs_path:%s' % (source_abs_path, target_abs_path))
            # subprocess.call('ffmpeg -i %s %s' % (source_abs_path, target_abs_path))
            # else:
            #     print('已存在.')
            # os.popen3('ffmpeg.exe -i %s %s' %s (source_abs_path,))

            # target_abs_path =
            # print("%s,隶属于 %s " % (nginx_path, os.path.dirname(nginx_path)))

            # 需要获取文件绝对路径, source+

            # 再需要获取输出路径.
    return bat_list


def convert_media():
    bat_list = create_ffmpeg_bat()
    # for i in bat_list:
    file_ = "command_cache.txt"
    if os.path.exists(file_):
        os.remove(file_)
    yy_utils.create_dirs(file_)
    with open(file_, 'w+') as f:
        for bat_line in bat_list:
            f.write(bat_line)

    with open(file_, 'r+') as f:
        data = f.readlines()  # txt中所有字符串读入data

        for line in data:
            print(line)


#
convert_media()
import subprocess

# cmd = '%s -i %s %s' % (
# os.path.abspath('./bats/ffmpeg'), os.path.abspath('./bats/1.mkv'), os.path.abspath('./bats/1.mp4'))
# print(cmd)
# subprocess.call(['./bats/ffmpeg','-i','./bats/1.mkv','./bats/1.mp4'])

# index += 1
# 负责生成bat文件.
# print('start')
# subprocess.call(
#     'ffmpeg -i F:/pywork/MrYangServer/static/media/sourceFile/源/英雄时刻_20171028-10点01分58s.avi F:/pywork/MrYangServer/static/media/targetFile/asdfwer/英雄时刻.mp4')
# print('success')
# os.popen3('ffmpeg.exe -i F:/static/media/video/1080.avi  F:/static/media/ffvideo/1080.mov')
# from glob import  glob


video = '/Users/mryang/Documents/git/django_work/MrYangServer/media_source/movie/电影1/[阳光电影www.ygdy8.net].银翼杀手2049.BD.720p.中英双字幕.mkv'
# metadata = skvideo.io.ffprobe(skvideo.datasets.bigbuckbunny())
# print(metadata.keys())
# print(json.dumps(metadata["video"], indent=4))

# def get_sorted_ts(user_path):
#     ts_list = glob(os.path.join(user_path,'*.ts'))
#     boxer = []
#     for ts in ts_list:

# get_sorted_ts(video)


# videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny())
# print(videodata.shape)

# imageio.plugins.ffmpeg.download()
# vid = imageio.get_reader(video, 'ffmpeg')
# for im in enumerate(vid):
#     print(vid)
#  #image的类型是mageio.core.util.Image可用下面这一注释行转换为arrary
#  #image = skimage.img_as_float(im).astype(np.float32)
# #     fig = pylab.figure()
# #     fig.suptitle('image #{}'.format(num), fontsize=20)
# #     pylab.imshow(image)
# # pylab.show()
