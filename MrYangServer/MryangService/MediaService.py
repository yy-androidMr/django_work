import json
import os
import shutil

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()
from MryangService.frames.ServiceInterface import s_loop
from Mryang_App.models import Media
from Tools.CacheTmpInfo import CacheTmpInfo
from frames import ypath, TmpUtil, yutils
from frames.xml import XMLMedia
from MryangService.utils import logger

#  进度校验的key 三个环节.
TMP_AUDIO_KEY = 'audio'
TMP_CONVERT_KEY = 'convert'
TMP_CUT_KEY = "cut"
STATE_INIT = 0
STATE_AUDIO_FINISH = 1  # 音频状态检查完毕
STATE_VIDOE_COMPRESS_FINISH = 2  # 视频转码完毕.
# --------------------

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'
mulit_audio_dir = 'media_mulit_audio'

movie_config = XMLMedia.get_infos()

cache_tmp_info = CacheTmpInfo()
ffmpeg_tools = TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
ffprobe_tools = TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
# 视频源路径
src_root = ypath.join(TmpUtil.src(), movie_config[XMLMedia.TAGS.DIR_ROOT])
# 其他音轨存放处
mulit_audio_path = ypath.join(TmpUtil.src(), mulit_audio_dir)
# 视频转码目标路径
convert_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.DIR_ROOT])
# 转码结束后的切片路径
m3u8_ts_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.TS_DIR])
# TmpUtil.clear_key(FFMPEG_KEY)
# TmpUtil.clear_key(FFPROBE_KEY)

logger.info('src_root:', src_root, 'convert_root:', convert_root, 'm3u8_ts_root:', m3u8_ts_root)

src_files = []
cur_file_info = {}


def cur_db():
    return cur_file_info.get('db')


def modify_state(media_db, state):
    media_db.state = state
    media_db.save()


def check_file(path):
    path = ypath.replace(path)
    if os.path.isdir(path):
        return False
    if mulit_audio_dir in path:
        return False
    # 如果这里没有该路径. 是不是应该删除?
    if cur_db() and os.path.exists(cur_db().abs_path) and os.path.samefile(
            cur_db().abs_path, path):
        return False
    return True


def delete(event, directory):
    pass
    # print(event.src_path, directory, 'delete')


def create(event, directory):
    if not check_file(event.src_path):
        return
    src_files.append(event.src_path)


def start():
    for root, dirs, files in os.walk(src_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            src_files.append(ypath.join(root, file))

    s_loop(loop)


def loop():
    if len(src_files) == 0:
        return False
    logger.info("MediaService一个流程:" + str(len(src_files)) + '   ' + src_files[0])
    compress(src_files[0])
    del src_files[0]
    return True


def compress(src_file):
    # 这里要做三步骤调用  1.音轨检查 2.格式转换(或者复制) 3.切片
    try:
        media_db = Media.objects.get(abs_path=src_file)
    except Exception:
        media_db = Media()
        media_db.abs_path = src_file
        media_db.state = STATE_INIT
        media_db.file_name = os.path.basename(src_file)
        media_db.save()
    cur_file_info['db'] = media_db
    analysis_audio_info(media_db)
    compress_video(media_db)
    # Media.objects.get()
    # if len(query_set) == 0:


def analysis_audio_info(media_db):
    def movie_info_res(cmdlist, _):
        if len(cmdlist) <= 0:
            modify_state(media_db, STATE_AUDIO_FINISH)
            return
        jsonbean = json.loads(''.join(cmdlist))

        streamlist = jsonbean['streams']
        format = jsonbean['format']
        media_db.md5 = yutils.get_md5(media_db.abs_path)
        media_db.duration = int(float(format['duration']))
        # cur_file_info['duration'] =
        media_db.size = int(format['size'])
        if len(streamlist) <= 0:
            modify_state(media_db, STATE_AUDIO_FINISH)
            return
        audio_streams = []
        decode_map = ''
        for stream_item in streamlist:
            if stream_item['codec_type'] == 'audio':
                logger.info(str(stream_item))
                audio_streams.append(stream_item)
            else:
                if stream_item['codec_type'] == 'video':
                    # 如果是视频.保存视频信息
                    media_db.codec_type = stream_item['codec_name']
                    media_db.codec_long_name = stream_item['codec_long_name']
                    media_db.width = int(stream_item['width'])
                    media_db.height = int(stream_item['height'])
                    try:
                        media_db.r_frame_rate = round(eval(stream_item['r_frame_rate']))
                        media_db.avg_frame_rate = round(eval(stream_item['avg_frame_rate']))
                    except ZeroDivisionError:
                        media_db.r_frame_rate = 0
                        media_db.avg_frame_rate = 0

                decode_map += ' -map 0:' + str(stream_item['index'])

        # 有多个语种
        digout = False
        if len(audio_streams) > 1:
            for audio_stream in audio_streams:
                if 'tags' in audio_stream and 'title' in audio_stream['tags'] \
                        and ('国语' == audio_stream['tags']['title'] or '中语' == audio_stream['tags']['title']):
                    decode_map += ' -map 0:' + str(audio_stream['index'])
                    digout = True
                    break
        else:
            logger.info('该视频音轨只有一个,不需要转换:' + media_db.abs_path)
            modify_state(media_db, STATE_AUDIO_FINISH)
            return

        if not digout:
            for audio_stream in audio_streams:
                decode_map += ' -map 0:' + str(audio_stream['index'])
            #     out_content += str(index) + ':' + str(audio_stream) + '\n'
            #     index += 1
            # select_audio = len(audio_streams)
            # while len(audio_streams) <= select_audio or select_audio < 0:
            #     select_audio = int(input(out_content + '选择音轨:'))

        # desc_file = file +
        _, desc_mulit_path = ypath.decompose_path(media_db.abs_path, src_root, mulit_audio_path)
        out_file = desc_mulit_path + '.chi' + ypath.file_exten(media_db.abs_path)
        if os.path.exists(out_file):
            os.remove(out_file)
        logger.info(out_file)

        copy_cmd = ffmpeg_tools + ' -i ' + media_db.abs_path + decode_map + '  -vcodec copy -acodec copy ' + out_file
        yutils.process_cmd(copy_cmd, done_call=rm_on_audio_copy, param=(media_db.abs_path, out_file, desc_mulit_path))

    # 音轨结束后,保存源文件到movie_otherformat目录,替换原有文件名.
    def rm_on_audio_copy(_, files):
        shutil.move(files[0], files[2])
        shutil.move(files[1], files[0])
        modify_state(media_db, STATE_AUDIO_FINISH)

    if media_db.state >= STATE_AUDIO_FINISH:
        logger.info('该文件的音轨已经转换过了:' + media_db.abs_path)
        return
    logger.info('开始转换:' + media_db.abs_path)
    yutils.process_cmd(
        ffprobe_tools + ' ' + media_db.abs_path + ' -print_format  json -show_format -show_streams',
        done_call=movie_info_res)


def compress_video(media_db):
    if media_db.state >= STATE_VIDOE_COMPRESS_FINISH:
        logger.info('该文件已经转码过了:' + media_db.abs_path)
        return

    # 这里需要有判断:如果文件流是h264的
    if media_db.codec_type == 'h264':
        print('这个视频是 h264流视频, 可以直接复制' + media_db.abs_path)
    else:
        print('这个视频不是:' + media_db.abs_path)
# del_audio_tags()
# convert_video()
#
# XMLMedia.create_media_item_info_xml(item_info_list)
