import os
import pickle

import yy_utils

cd_count = '../' * 3

source_root = ''.join([cd_count, yy_utils.media_source, '/movie/src'])
target_root = ''.join([cd_count, yy_utils.media_source, '/movie/desc'])
net_static_root = ''.join([cd_count, yy_utils.static_media_root, '/movie'])



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
            source_abs_path = os.path.abspath(source_rela_path)
            target_abs_path = os.path.abspath(target_root) + '\\' + file_name + '.mp4'
            target_abs_path = target_abs_path.replace('\\', '/').replace('//', '/')
            yy_utils.create_dirs(target_abs_path)
            peg = os.path.abspath('output/exe/ffmpeg')
            bat_list.append('%s -i %s -d 900 %s' % (peg, source_abs_path, target_abs_path))

    return bat_list


def create_convert_bats():
    bat_list = create_ffmpeg_bat()
    dir = "output/"
    yy_utils.create_dirs(dir)
    index = 0
    for bat_line in bat_list:
        # name = '%d.sh' % index
        file_ = ''.join([dir, str(index), '.sh' if yy_utils.is_mac() else '.bat'])
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
                source_rela_path = os.path.join(root, file)
                target_dir = '/'.join([net_static_root, yy_utils.md5_of_str(source_rela_path)])
                # if os.path.exists(target_dir):
                #     # 不做处理.重复切片
                #     pass
                # else:
                yy_utils.create_dirs(target_dir, True)
                info = {}
                info['name'] = os.path.basename(file)
                pickle_file = open(''.join([target_dir, '/info']), 'wb')
                pickle.dump(info, pickle_file)  # 只能以二进制写入
                pickle_file.close()
                # with open(''.join([target_dir, '/info']), 'w+') as f:
                #     f.write('')  # 需要写入信息.使用二进制?


cut_video()
