import os
import pickle

import sys

from Mryang_App import yutils

cd_count = '../' * 4

source_root = ''.join([cd_count, yutils.media_source, '/movie/src'])
target_root = ''.join([cd_count, yutils.media_source, '/movie/desc'])
net_static_root = ''.join([cd_count, yutils.static_media_root, '/movie'])


def create_ffmpeg_bat():
    bat_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            (_, source_abs_path, target_abs_path, _) = yutils.decompose_path(
                root, file, source_root, target_root, exten='.mp4')
            peg = os.path.abspath('output/exe/ffmpeg')
            bat_list.append('%s -i %s -d 900 %s' % (peg, source_abs_path, target_abs_path))

    return bat_list


# 生成ffmpeg的bat文件,提供批量转换.
def create_convert_bats():
    bat_list = create_ffmpeg_bat()
    dir = "output/"
    yutils.create_dirs(dir)
    index = 0
    for bat_line in bat_list:
        # name = '%d.sh' % index
        file_ = ''.join([dir, str(index), '.sh' if yutils.is_mac() else '.bat'])
        index += 1
        with open(file_, 'w+') as f:
            f.write(bat_line)


# 第二需求: 视频切片
def cut_video():
    # 假设已经读取了
    infos = ''
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if '.mp4' in file.lower():
                (rela_file_name, source_abs_path, target_abs_path, target_rela_path) = yutils.decompose_path(root, file,
                                                                                                             target_root,
                                                                                                             net_static_root)
                # source_rela_path = os.path.join(root, file)



                target_dir = yutils.file_name(target_abs_path) + yutils.M3U8_DIR_EXTEN
                if os.path.exists(target_dir):
                    # 不做处理.重复切片
                    print('cut exists %s %s' % (source_abs_path, target_dir))
                    pass
                else:
                    yutils.create_dirs(target_dir, True)
                    info = {}  # map形式存储
                    info['name'] = yutils.file_name(os.path.basename(file))
                    with open(''.join([target_dir, '/info']), 'wb') as f:
                        pickle.dump(info, f)  # 只能以二进制写入

                    peg = os.path.abspath('output/exe/ffmpeg')
                    to_path = target_dir

                    cmd = peg + ' -i ' + source_abs_path + ' -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list ' + to_path + '\\' + yutils.M3U8_NAME + ' -segment_time 5 ' + to_path + r'\%03d.ts'
                    print(cmd)
                    os.system(cmd)
                    # with open(''.join([target_dir, '/info']), 'w+') as f:
                    #     f.write('')  # 需要写入信息.使用二进制?


if __name__ == '__main__':
    cut_video()
# create_convert_bats()

# import subprocess
# output = subprocess.Popen("/usr/local/ffmpeg/bin/ffmpeg -i '" + r"G:\pyWorkspace\django_work\MrYangServer\media_source\movie\src\香水BD中字[电影天堂www.dy2018.com].mp4" + "' 2>&1 | grep 'Duration'", shell=True,
#                           stdout=subprocess.PIPE).stdout.read()
#
# print(output)
