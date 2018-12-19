import os
import pickle
import shutil
import sys

import time

sys.path.append('../../..')

from frames import yutils, logger

# source_root = ''.join([yutils.media_source, '/movie/src'])
# target_root = ''.join([yutils.media_source, '/movie/desc'])
FFMPEG_KEY = 'FFMPEG_KEY'

net_static_root = 'G:\cache\work_cache/resource_desc_root\movie/out'  # '''.join([yutils.media_source, '/movie'])
net_ts_root = 'G:\cache\work_cache/resource_desc_root\movie/ts'  # .join([yutils.media_source, '/movie_ts'])
DIR_ROOT = 'movie'


def done_call(_, param):
    for k in param:
        logger.info('消耗时间:%d,命令:%s' % (param[k], k))


def convert_video():
    bat_list = create_ffmpeg_bat()
    logger.info('准备转换:%s' % str(bat_list))
    for bat in bat_list:
        cur_time = int(time.time())
        logger.info('开始时间:%d,转换命令:%s' % (cur_time, bat))
        yutils.process_cmd(bat, done_call=done_call, param={bat: cur_time})


def create_ffmpeg_bat():
    bat_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            (_, source_abs_path, target_abs_path, _) = yutils.decompose_path(
                root, file, source_root, target_root, exten='.mp4')
            if os.path.exists(target_abs_path):
                continue
            yutils.create_dirs(target_abs_path)
            if '.mp4' in file:
                shutil.copy(source_abs_path, target_abs_path)
                continue
            # '%s -i %s -d 900 %s'

            bat_list.append('%s -i %s %s' % (ffmpeg_tools, source_abs_path, target_abs_path))

    return bat_list


# 第二需求: 视频切片
def create_ts(root, file, last_path):
    (_, _, _, target_rela_path_ts) = yutils.decompose_path(root, file, target_root, net_ts_root)
    ts_dir = os.path.dirname(target_rela_path_ts) + last_path

    return ts_dir


def cut_call(str):
    pass


def cut_end(_, param):
    print('end')


def cut_video():
    # 假设已经读取了
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if '.mp4' in file.lower():
                (_, source_abs_path, target_abs_path, target_rela_path) = yutils.decompose_path(root, file,
                                                                                                target_root,
                                                                                                net_static_root)
                # source_rela_path = os.path.join(root, file)
                last_path = '/' + yutils.md5_of_str(os.path.basename(target_abs_path)) + yutils.M3U8_DIR_EXTEN
                target_dir = os.path.dirname(target_rela_path) + last_path

                ts_dir = create_ts(root, file, last_path)
                print(target_dir)
                # if os.path.exists(target_dir):
                if False:
                    # 不做处理.重复切片
                    print('cut exists %s %s' % (source_abs_path, target_dir))
                    pass
                else:
                    yutils.create_dirs(target_dir, True)
                    yutils.create_dirs(ts_dir, True, True)
                    info = {}  # map形式存储
                    info[yutils.MOVIE_INFO_NAME] = yutils.file_name(os.path.basename(file))
                    with open(''.join([target_dir, '/info']), 'wb') as f:
                        pickle.dump(info, f)  # 只能以二进制写入

                    cmd = ffmpeg_tools + ' -i ' + source_abs_path + ' -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list ' + target_dir + '/' + yutils.M3U8_NAME + ' -segment_time 5 ' + ts_dir + '/%03d.ts'
                    print(cmd)
                    yutils.process_cmd(cmd, done_call=cut_end)
                    print('done:' + target_dir)


if __name__ == '__main__':
    # def run():
    source_root = yutils.input_path(yutils.RESOURCE_ROOT_KEY,
                                    '请指定资源根目录(例如:E:/resource_root),目录下有个%s文件夹,并且%s下就是图片:\n' % (DIR_ROOT, DIR_ROOT))
    source_root = os.path.join(source_root, DIR_ROOT)
    target_root = yutils.input_path(yutils.RESOURCE_DESC_KEY,
                                    '请指定资源输出目录(例如:E:/resource_desc_root),目录下会创建%s/convert和%s/ts):\n' % (
                                        DIR_ROOT, DIR_ROOT))
    target_root = os.path.join(target_root, DIR_ROOT, 'convert')
    ffmpeg_tools = yutils.input_path(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')

    cut_video()
    # create_convert_bats()
