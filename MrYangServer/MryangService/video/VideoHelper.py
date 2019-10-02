import json
import os
import shutil
import threading
from pathlib import Path

from django.db import transaction

from MryangService.mpath import MediaPath
from Mryang_App.DBHelper import MediaHelp

# 这里需要制作一下 删除src没有的所有文件文件夹. 是否需要抽出成一个公共函数?
from Mryang_App.models import Media, MPath
from frames import yutils, ypath, logger

lock = threading.Lock()


# 删除本地不存在的数据
def handle_meida_db_exists(src_root_list):
    posix_file_list = []
    for dir in src_root_list:
        posix_file_list.extend([ypath.convert_path(file.as_posix()) for file in Path(dir).rglob('*.*')])
    all_media_set = Media.objects.all()
    with transaction.atomic():
        for media_db in all_media_set:
            if media_db.abs_path not in posix_file_list:
                media_db.delete()


# 获取到media的数据库字段.
def get_media_db(file_path, dm_dict):
    if os.path.isdir(file_path):
        return None
    if not yutils.is_movie(file_path):
        return None
    file = ypath.convert_path(file_path)
    media_db_query = Media.objects.filter(abs_path=file)
    cur_media_db = None
    if len(media_db_query) > 0:
        cur_media_db = media_db_query[0]
    else:
        # target = ypath.decompose_path(
        #     file, str(media_src_root), str(convert_root), exten='.mp4')
        media_db = Media()
        media_db.abs_path = file
        media_db.state = MediaHelp.STATE_INIT
        media_db.file_name = os.path.basename(file)
        # media_db.desc_path = target
        # media_db.nginx_path = target.replace(str(convert_root.as_posix()), '')
        # create_db_list.append(media_db)
        media_db.folder_key = dm_dict[os.path.dirname(file)]
    pass


def compress(media_db):
    if MediaHelp.is_err(media_db.state):
        return


# 转码音频
def analysis_audio_info(media_db, ffprobe_tools, ffmpeg_tools, mulit_audio_dir, mpath: MPath):
    def movie_info_res(cmdlist, _):
        if len(cmdlist) <= 0:
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
            return
        jsonbean = json.loads(''.join(cmdlist))
        if 'streams' not in jsonbean.keys():
            modify_state(media_db, MediaHelp.STATE_SRC_ERROR)
            return
        streamlist = jsonbean['streams']
        format = jsonbean['format']
        media_db.md5 = yutils.get_md5(media_db.abs_path)
        media_db.duration = int(float(format['duration']))
        # cur_file_info['duration'] =
        media_db.size = int(format['size'])
        if len(streamlist) <= 0:
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
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
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
            return

        if not digout:
            for audio_stream in audio_streams:
                decode_map += ' -map 0:' + str(audio_stream['index'])
            #     out_content += str(index) + ':' + str(audio_stream) + '\n'
            #     index += 1
            # select_audio = len(audio_streams)
            # while len(audio_streams) <= select_audio or select_audio < 0:
            #     select_audio = int(input(out_content + '选择音轨:'))

        # mulit_audio_path = TmpUtil.src() / movie_config.base_info.mulit_audio_dir
        # out_file = desc_mulit_path + '.chi' + ypath.file_exten(media_db.abs_path)
        # ypath.create_dirs(desc_mulit_path)
        # if os.path.exists(out_file):
        #     os.remove(out_file)
        # logger.info(out_file)
        with lock:
            mulit_audio_path = ypath.join(MediaPath.src(), mulit_audio_dir)
        desc_mulit_path = ypath.decompose_path(media_db.abs_path, str(mpath.pa), str(mulit_audio_path))

        copy_cmd = ffmpeg_tools + ' -i \"' + media_db.abs_path + '\"' + decode_map + '  -vcodec copy -acodec copy \"' + out_file + '\"'
        yutils.process_cmd(copy_cmd, done_call=rm_on_audio_copy, param=(media_db.abs_path, out_file, desc_mulit_path))

    if MediaHelp.is_err(media_db.state):
        return

    # 音轨结束后,保存源文件到movie_otherformat目录,替换原有文件名.
    def rm_on_audio_copy(_, files):
        shutil.move(files[0], files[2])
        shutil.move(files[1], files[0])
        modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)

    if media_db.state >= MediaHelp.STATE_AUDIO_FINISH:
        logger.info('该文件的音轨已经转换过了:' + media_db.abs_path)
        return
    logger.info('开始转换:' + media_db.abs_path)
    yutils.process_cmd(
        ffprobe_tools + ' \"' + media_db.abs_path + '\" -print_format  json -show_format -show_streams',
        done_call=movie_info_res)


def modify_state(media_db, state):
    media_db.state = state
    media_db.save()
