import os
import pickle
import shutil
import sys

import time

sys.path.append('../../..')
from frames import yutils, logger, ypath, DataBean
from frames.xml import XMLMovie, XMLBase

FFMPEG_KEY = 'FFMPEG_KEY'

movie_config = XMLMovie.get_infos()


def DoneConvertCall(_, param):
    logger.info('消耗时间:%d,命令:%s' % (param['time'], param['cmd']))
    if (param['last']):
        # 最后一个做操作
        logger.info('执行转换完成!,开始切割视频')
        CutVideo()


def ConvertVideo():
    bat_list = CreatePegCmd()
    logger.info('准备转换:%s' % str(bat_list))
    index = 0
    if len(bat_list) > 0:
        for bat in bat_list:
            cur_time = int(time.time())
            logger.info('开始时间:%d,转换命令:%s' % (cur_time, bat))
            yutils.process_cmd(bat, done_call=DoneConvertCall,
                               param={'cmd': bat, 'time': cur_time, 'last': (index + 1 == len(bat_list))})
            index += 1
    else:
        CutVideo()


def CreatePegCmd():
    bat_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
                # src_path = join(src_file_root, src_file_name)
            src_path = ypath.join(root, file)

            (_, target) = ypath.decompose_path(
                src_path, source_root, target_root, exten='.mp4')
            if os.path.exists(target):
                continue
            yutils.create_dirs(target)
            if '.mp4' in file:
                logger.info('begin copy \"%s\"' % file)
                shutil.copy(src_path, target)
                continue
            # '%s -i %s -d 900 %s'

            bat_list.append('\"%s\" -i \"%s\" \"%s\"' % (ffmpeg_tools, src_path, target))

    return bat_list


def ItemInfo(file, last_path):
    info = {}
    info[XMLMovie.ITEM_TAGS.FILE] = file
    info[XMLMovie.ITEM_TAGS.NAME] = ypath.file_name(file)
    info[XMLMovie.ITEM_TAGS.SIZE] = str(os.path.getsize(file))
    info[XMLMovie.ITEM_TAGS.SHOW_SIZE] = yutils.fileSizeConvert(int(info[XMLMovie.ITEM_TAGS.SIZE]))
    info[XMLMovie.ITEM_TAGS.OUT_NAME] = last_path

    # 读取视频信息.
    video_info = yutils.video_info(file)
    info[XMLMovie.ITEM_TAGS.PIXEL] = str(video_info[XMLMovie.ITEM_TAGS.PIXEL])
    info[XMLMovie.ITEM_TAGS.FPS] = str(round(video_info[XMLMovie.ITEM_TAGS.FPS]))
    info[XMLMovie.ITEM_TAGS.DURATION] = str(int(video_info[XMLMovie.ITEM_TAGS.DURATION]))
    info[XMLMovie.ITEM_TAGS.SHOW_DURATION] = yutils.time_convert(int(info[XMLMovie.ITEM_TAGS.DURATION]))
    return info


def CutVideo():
    # 假设已经读取了
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if '.mp4' in file.lower():
                # 获取源文件路径
                src_path = ypath.join(root, file)
                # 拼写输出文件名
                rename = yutils.md5_of_str(os.path.basename(src_path)) + movie_config[XMLMovie.TAGS.DIR_EXTEN]
                # 获取输出文件路径
                (rela_file_name, target_path) = ypath.decompose_path(src_path, target_root, out_root, rename=rename)

                # 添加xml信息.
                item_info_list.append(ItemInfo(src_path, rela_file_name))
                if os.path.exists(target_path):
                    # if False:
                    # 不做处理.重复切片
                    logger.info('已存在: %s %s' % (src_path, target_path))
                    pass
                else:
                    m3u8_file = ypath.join(target_path, movie_config[XMLMovie.TAGS.NAME])
                    yutils.create_dirs(m3u8_file)
                    cmd = '\"' + ffmpeg_tools + '\" -i \"' + src_path + '\" -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list \"' + m3u8_file + '\" -segment_time 5 \"' + target_path + '/%04d.ts\"'
                    yutils.process_cmd(cmd)
                    logger.info('切割完成:' + target_path)


if __name__ == '__main__':
    dir_root = movie_config[XMLMovie.TAGS.DIR_ROOT]
    source_root = yutils.input_path(yutils.RESOURCE_ROOT_KEY,
                                    '请指定资源根目录(例如:E:/resource_root),目录下有个%s文件夹,并且%s下就是图片:\n' % (dir_root, dir_root))
    source_root = ypath.join(source_root, dir_root)
    target_root = yutils.input_path(yutils.RESOURCE_DESC_KEY,
                                    '请指定资源输出目录(例如:E:/resource_desc_root),目录下会创建%s/convert和%s/ts):\n' % (
                                        dir_root, dir_root))
    target_root = ypath.join(target_root, dir_root)
    ffmpeg_tools = yutils.input_path(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')

    out_root = XMLMovie.get_out_root()
    item_info_list = []
    ConvertVideo()
    XMLMovie.create_movie_item_info_xml(item_info_list)
