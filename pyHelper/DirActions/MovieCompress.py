import os
import urllib

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
            print('source_abs_path:%s ,target_abs_path:%s' % (source_abs_path, target_abs_path))
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
    index = 0
    for i in bat_list:
        file_ = "../bats/%s.bat" % index
        index += 1
        if os.path.exists(file_):
            os.remove(file_)
        yy_utils.create_dirs(file_)
        with open(file_, 'w+') as f:
            f.write(i)


convert_media()
# index += 1
# 负责生成bat文件.
# print('start')
# subprocess.call(
#     'ffmpeg -i F:/pywork/MrYangServer/static/media/sourceFile/源/英雄时刻_20171028-10点01分58s.avi F:/pywork/MrYangServer/static/media/targetFile/asdfwer/英雄时刻.mp4')
# print('success')
# os.popen3('ffmpeg.exe -i F:/static/media/video/1080.avi  F:/static/media/ffvideo/1080.mov')
