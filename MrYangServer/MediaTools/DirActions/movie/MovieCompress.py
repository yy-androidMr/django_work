import os
import pickle
import shutil
import sys

import time

sys.path.append('../../..')
from frames import yutils, logger, DataBean
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
            (_, source_abs_path, target_abs_path, _) = yutils.decompose_path(
                root, file, source_root, target_root, exten='.mp4')
            if os.path.exists(target_abs_path):
                continue
            yutils.create_dirs(target_abs_path)
            if '.mp4' in file:
                logger.info('begin copy \"%s\"' % file)
                shutil.copy(source_abs_path, target_abs_path)
                continue
            # '%s -i %s -d 900 %s'

            bat_list.append('\"%s\" -i \"%s\" \"%s\"' % (ffmpeg_tools, source_abs_path, target_abs_path))

    return bat_list


def ItemInfo(file, last_path):
    info = {}
    info[XMLMovie.ITEM_TAGS.FILE] = file
    info[XMLMovie.ITEM_TAGS.NAME] = yutils.file_name(os.path.basename(file))
    info[XMLMovie.ITEM_TAGS.SIZE] = str(os.path.getsize(file))
    info[XMLMovie.ITEM_TAGS.SHOW_SIZE] = yutils.fileSizeConvert(int(info[XMLMovie.ITEM_TAGS.SIZE]))
    from moviepy.editor import VideoFileClip
    info[XMLMovie.ITEM_TAGS.DURATION] = str(VideoFileClip(file).duration)
    info[XMLMovie.ITEM_TAGS.SHOW_DURATION] = yutils.time_convert(float(info[XMLMovie.ITEM_TAGS.DURATION]))
    info[XMLMovie.ITEM_TAGS.OUT_NAME] = last_path
    return info


def CutVideo():
    # 假设已经读取了
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if '.mp4' in file.lower():
                (_, source_abs_path, target_abs_path, target_rela_path) = yutils.decompose_path(root, file,
                                                                                                target_root,
                                                                                                out_root)
                # '48ac8a3d45a37c9f636955187f11e445.ym3'
                last_path = yutils.md5_of_str(os.path.basename(target_abs_path)) + movie_config[
                    XMLMovie.TAGS.DIR_EXTEN]
                # 'G:/cache/work_cache/resource_desc_root\\movie\\out\\48ac8a3d45a37c9f636955187f11e445.ym3'
                target_dir = os.path.join(os.path.dirname(target_rela_path), last_path)

                m3u8_file = os.path.join(target_dir, movie_config[XMLMovie.TAGS.NAME])
                item_info_list.append(ItemInfo(source_abs_path, last_path))
                if os.path.exists(target_dir):
                    # if False:
                    # 不做处理.重复切片
                    logger.info('cut exists %s %s' % (source_abs_path, target_dir))
                    pass
                else:
                    yutils.create_dirs(m3u8_file)
                    cmd = '\"' + ffmpeg_tools + '\" -i \"' + source_abs_path + '\" -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list \"' + m3u8_file + '\" -segment_time 5 \"' + target_dir + '/%04d.ts\"'
                    yutils.process_cmd(cmd)
                    logger.info('切割完成:' + target_dir)


if __name__ == '__main__':
    dir_root = movie_config[XMLMovie.TAGS.DIR_ROOT]
    source_root = yutils.input_path(yutils.RESOURCE_ROOT_KEY,
                                    '请指定资源根目录(例如:E:/resource_root),目录下有个%s文件夹,并且%s下就是图片:\n' % (dir_root, dir_root))
    source_root = os.path.join(source_root, dir_root)
    target_root = yutils.input_path(yutils.RESOURCE_DESC_KEY,
                                    '请指定资源输出目录(例如:E:/resource_desc_root),目录下会创建%s/convert和%s/ts):\n' % (
                                        dir_root, dir_root))
    target_root = os.path.join(target_root, dir_root)
    ffmpeg_tools = yutils.input_path(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')

    out_root = XMLMovie.get_out_root()
    item_info_list = []
    ConvertVideo()
    XMLMovie.create_movie_item_info_xml(item_info_list)
