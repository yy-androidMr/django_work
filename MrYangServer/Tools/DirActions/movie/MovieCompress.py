import os
import pickle

from Tools.CacheTmpInfo import CacheTmpInfo
from frames import yutils, logger, ypath, Globals
from frames.xml import XMLMovie
import shutil
import sys
import json
import time

sys.path.append('../../..')

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'

#  进度校验的key
TMP_AUDIO_KEY = 'audio'
TMP_CONVERT_KEY = 'convert'
TMP_CUT_KEY = "cut"
# --------------------

# 这里存放多音轨的视频源文件
other_format_dir = 'media_mulit_audio'
movie_config = XMLMovie.get_infos()


def done_convert_call(_, param):
    logger.info('消耗时间:%d,命令:%s' % (param['time'], param['cmd']))
    if param['last']:
        # 最后一个做操作
        logger.info('执行转换完成!,开始切割视频')
        cache_tmp_info.write_info(param['src_path'], TMP_CONVERT_KEY, True)
        cut_video()


def convert_video():
    bat_list = create_peg_cmd()
    logger.info('准备转换:%s' % str(bat_list))
    index = 0
    if len(bat_list) > 0:
        for src_path in bat_list:
            cur_time = int(time.time())
            logger.info('开始时间:%d,转换命令:%s' % (cur_time, bat_list[src_path]))
            yutils.process_cmd(bat_list[src_path], done_call=done_convert_call,
                               param={'cmd': bat_list[src_path], 'time': cur_time,
                                      'last': (index + 1 == len(bat_list)), 'src_path': src_path})
            index += 1
    else:
        cut_video()


def create_peg_cmd():
    bat_list = {}
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            src_path = ypath.join(root, file)

            (_, target) = ypath.decompose_path(
                src_path, src_root, convert_root, exten='.mp4')
            if os.path.exists(target):
                if cache_tmp_info.tmp_info(src_path).get(TMP_CONVERT_KEY):
                    continue
                else:
                    os.remove(target)
                # rename = yutils.md5_of_str(os.path.basename(src_path)) + movie_config[XMLMovie.TAGS.DIR_EXTEN]
                # (rela_file_name, target_path) = ypath.decompose_path(src_path, convert_root, m3u8_ts_root,
                #                                                      rename=rename)
                # if os.path.exists(rela_file_name):
                #     continue
                # else:
                #     pass

            ypath.create_dirs(target)
            if '.mp4' in file:
                logger.info('begin copy \"%s\"' % file)
                shutil.copy(src_path, target)
                continue
            # threads有效 但是需要在多核中测试
            bat_list[src_path] = '\"%s\" -i \"%s\"  \"%s\"' % (ffmpeg_tools, src_path, target)

    return bat_list


def item_info(file, last_path):
    size = os.path.getsize(file)
    video_info = yutils.video_info(file)

    info = {
        XMLMovie.ITEM_TAGS.FILE: file,
        XMLMovie.ITEM_TAGS.NAME: ypath.file_name(file),
        XMLMovie.ITEM_TAGS.SIZE: str(size),
        XMLMovie.ITEM_TAGS.SHOW_SIZE: yutils.fileSizeConvert(size),
        XMLMovie.ITEM_TAGS.OUT_NAME: last_path,
        # 读取视频信息.
        XMLMovie.ITEM_TAGS.PIXEL: str(video_info[XMLMovie.ITEM_TAGS.PIXEL]),
        XMLMovie.ITEM_TAGS.FPS: str(round(video_info[XMLMovie.ITEM_TAGS.FPS])),
        XMLMovie.ITEM_TAGS.DURATION: str(int(video_info[XMLMovie.ITEM_TAGS.DURATION])),
        XMLMovie.ITEM_TAGS.SHOW_DURATION: yutils.time_convert(int(video_info[XMLMovie.ITEM_TAGS.DURATION]))
    }
    return info


def cut_video():
    # 假设已经读取了
    for root, dirs, files in os.walk(convert_root):
        for file in files:
            if '.mp4' in file.lower():
                # 获取源文件路径
                src_path = ypath.join(root, file)
                # 拼写输出文件名
                rename = yutils.md5_of_str(os.path.basename(src_path)) + movie_config[XMLMovie.TAGS.DIR_EXTEN]
                # 获取输出文件路径
                (rela_file_name, target_path) = ypath.decompose_path(src_path, convert_root, m3u8_ts_root,
                                                                     rename=rename)
                # 必须要在这添加xml信息. 每次运行都会替换掉原先的配置.
                item_info_list.append(item_info(src_path, rela_file_name))

                if os.path.exists(target_path):
                    if cache_tmp_info.tmp_info(src_path).get(TMP_CUT_KEY):
                        # if False:
                        # 不做处理.重复切片
                        logger.info('已存在: %s %s' % (src_path, target_path))
                        return
                    else:
                        shutil.rmtree(target_path)
                m3u8_file = ypath.join(target_path, movie_config[XMLMovie.TAGS.NAME])
                ypath.create_dirs(m3u8_file)
                cmd = '\"' + ffmpeg_tools + '\" -i \"' + src_path + \
                      '\" -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list \"' + \
                      m3u8_file + '\" -segment_time 10 \"' + target_path + '/%05d.ts\"'

                yutils.process_cmd(cmd)
                logger.info('切割完成:' + target_path)


# 音轨结束后,保存源文件到movie_otherformat目录,替换原有文件名.
def rm_on_audio_copy(_, files):
    _, desc_file = ypath.decompose_path(files[0], src_root, movie_otherformat)
    # file_list.append(desc_file)
    ypath.create_dirs(desc_file)
    shutil.move(files[0], desc_file)
    # os.remove(files[0])
    os.rename(files[1], files[0])
    cache_tmp_info.write_info(files[0], TMP_AUDIO_KEY, True)


def movie_info_res(cmdlist, file):
    if len(cmdlist) <= 0:
        cache_tmp_info.write_info(file, TMP_AUDIO_KEY, True)
        return
    jsonbean = json.loads(''.join(cmdlist))
    streamlist = jsonbean['streams']
    if len(streamlist) <= 0:
        cache_tmp_info.write_info(file, TMP_AUDIO_KEY, True)
        return
    audio_streams = []
    decode_map = ''
    for stream_item in streamlist:
        if stream_item['codec_type'] == 'audio':
            logger.info(str(stream_item))
            audio_streams.append(stream_item)
        else:
            decode_map += ' -map 0:' + str(stream_item['index'])

    # 有多个语种
    digout = False
    if len(audio_streams) > 1:
        for audio_stream in audio_streams:
            if 'tags' in audio_stream and 'title' in audio_stream['tags'] and '国语' == audio_stream['tags']['title']:
                decode_map += ' -map 0:' + str(stream_item['index'])
                digout = True
                break
    else:
        logger.info('该视频音轨只有一个,不需要转换:' + file)
        cache_tmp_info.write_info(file, TMP_AUDIO_KEY, True)
        return

    if not digout:
        out_content = file + '\n没有找到对应音轨,自行选择:\n'
        index = 0
        for audio_stream in audio_streams:
            out_content += str(index) + ':' + str(audio_stream) + '\n'
            index += 1
        select_audio = len(audio_streams)
        while len(audio_streams) <= select_audio or select_audio < 0:
            select_audio = int(input(out_content + '选择音轨:'))

        decode_map += ' -map 0:' + str(audio_streams[select_audio]['index'])

    desc_file = file + '.chi' + ypath.file_exten(file)
    if os.path.exists(desc_file):
        os.remove(desc_file)
    logger.info(desc_file)
    # yutils.process_cmd('dir', done_call=rm_on_audio_copy, param=(file, desc_file))
    copy_cmd = ffmpeg_tools + ' -i ' + file + decode_map + '  -vcodec copy -acodec copy ' + desc_file
    yutils.process_cmd(copy_cmd, done_call=rm_on_audio_copy, param=(file, desc_file))


# 删除多余音轨,移动文件到备用目录
def del_audio_tags():
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            src_file = ypath.join(root, file)

            if cache_tmp_info.tmp_info(src_file).get(TMP_AUDIO_KEY):
                logger.info('该文件的音轨已经转换过了:' + src_file)
                continue
            # with open(ypath.join(TmpUtil.desc_tmp(),tmp_file_name),'rb') as fp:
            # fp.re

            logger.info('开始转换:' + src_file)
            yutils.process_cmd(
                # '/Users/mr.yang/Documents/res/src/ffmpeg.bin -i /Users/mr.yang/Documents/res/src/1.mkv -map 0:0 -map 0:2  -vcodec copy -acodec copy /Users/mr.yang/Documents/res/src/out.mkv',
                ffprobe_tools + ' ' + src_file + ' -print_format json -show_streams',
                # '/Users/mr.yang/Documents/res/src/ffprobe.bin /Users/mr.yang/Documents/res/src/1.mkv -print_format json -show_streams -select_streams a -hide_banner',
                done_call=movie_info_res, param=src_file)

    # for file in file_list:
    #     yutils.process_cmd(
    #         # '/Users/mr.yang/Documents/res/src/ffmpeg.bin -i /Users/mr.yang/Documents/res/src/1.mkv -map 0:0 -map 0:2  -vcodec copy -acodec copy /Users/mr.yang/Documents/res/src/out.mkv',
    #         ffprobe_tools + ' ' + file + ' -print_format json -show_streams',
    #         # '/Users/mr.yang/Documents/res/src/ffprobe.bin /Users/mr.yang/Documents/res/src/1.mkv -print_format json -show_streams -select_streams a -hide_banner',
    #         done_call=movie_info_res)
    #
    #     print(file)
    pass


if __name__ == '__main__':
    from frames import TmpUtil

    # 视频源路径
    src_root = ypath.join(TmpUtil.src(), movie_config[XMLMovie.TAGS.DIR_ROOT])
    # 非mp4格式视频存放处
    movie_otherformat = ypath.join(TmpUtil.src(), other_format_dir)
    # 视频转码目标路径
    convert_root = ypath.join(TmpUtil.desc(), movie_config[XMLMovie.TAGS.DIR_ROOT])
    # 转码结束后的切片路径
    m3u8_ts_root = ypath.join(TmpUtil.desc(), movie_config[XMLMovie.TAGS.TS_DIR])
    # TmpUtil.clear_key(FFMPEG_KEY)
    # TmpUtil.clear_key(FFPROBE_KEY)
    ffmpeg_tools = TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
    ffprobe_tools = TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n')

    logger.info('src_root:', src_root, 'convert_root:', convert_root, 'm3u8_ts_root:', m3u8_ts_root)
    item_info_list = []
    cache_tmp_info = CacheTmpInfo()
    del_audio_tags()
    convert_video()
    #
    XMLMovie.create_movie_item_info_xml(item_info_list)
