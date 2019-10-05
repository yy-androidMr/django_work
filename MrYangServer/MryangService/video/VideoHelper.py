import json
import os
import random
import shutil
import threading
from pathlib import Path

from PIL import Image
from django.db import transaction

from MryangService import ServiceHelper
from MryangService.mpath import MediaPath
from MryangService.utils import EmailUtil
from Mryang_App.DBHelper import MediaHelp

# 这里需要制作一下 删除src没有的所有文件文件夹. 是否需要抽出成一个公共函数?
from Mryang_App.models import Media, MPath, Dir
from frames import yutils, ypath, logger, Globals, TmpUtil
from frames.xml import XMLBase

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'
movie_config = XMLBase.list_cfg_infos('media_info')  # XMLMedia.get_infos()
src_root = movie_config.dir_root
ffmpeg_tools = str(TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
ffprobe_tools = str(
    TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
mulit_audio_dir = movie_config.base_info.mulit_audio_dir

lock = threading.Lock()

def src_dbs():
    return MediaPath.pdc().src_list


def media_root(dir_root):
    return ypath.join(dir_root, src_root)


def desc_path(media_db: Media):
    return ypath.join(media_root(media_db.desc_mpath.path), media_db.desc_path)


# 检查该状态是否正确
def check_media_db_state(media_db: Media):
    if media_db.state == MediaHelp.STATE_AUDIO_FINISH:
        if not os.path.exists(media_db.abs_path):
            media_db.state = MediaHelp.STATE_INIT
    if media_db.state == MediaHelp.STATE_VIDOE_COMPRESS_FINISH or media_db.state == MediaHelp.STATE_VIDEO_TS:
        if not os.path.exists(media_db.abs_path) or media_db.desc_mpath == None:
            media_db.state = MediaHelp.STATE_INIT
        desc = desc_path(media_db)  # ypath.join(media_db.desc_mpath.path, media_db.desc_path)
        if not os.path.exists(desc):
            media_db.state = MediaHelp.STATE_AUDIO_FINISH

    # 创建dir 目录


def gen_dir():
    def db_dir_exist(db_dirs):
        # dir不存在则删除.
        exist_pic_dirs = {}
        for pic_db in db_dirs:
            digout = False
            for src_db in src_dbs():
                if media_root(src_db.path) in pic_db.abs_path and os.path.isdir(pic_db.abs_path):
                    exist_pic_dirs[pic_db.abs_path] = pic_db
                    digout = True
                    break
            if not digout:
                pic_db.delete()
        return exist_pic_dirs

    def get_db_dirs():
        for dir in src_dbs():
            ypath.del_none_dir(media_root(dir.path))
        all_pic_dirs = Dir.objects.filter(type=yutils.M_FTYPE_MOIVE)
        db_dirs = db_dir_exist(all_pic_dirs)
        return db_dirs

    def folder_call(folder_list, is_root):
        if is_root:
            return
        # if is_root:
        #     if folder_list.path not in exist_pic_dirs:
        #         exist_pic_dirs[folder_list.path] = ServiceHelper.create_dir(exist_pic_dirs, folder_list,
        #                                                                     yutils.M_FTYPE_MOIVE)
        #     return
        save_list = []
        for dir in folder_list:
            if dir.path not in exist_media_dirs:
                db_dir = ServiceHelper.create_dir(exist_media_dirs, dir,
                                                  yutils.M_FTYPE_MOIVE, save_it=False)
                exist_media_dirs[dir.path] = db_dir
                save_list.append(db_dir)
                # PicHelper.handle_files_md5(src_file, dir_md5)
        for save in save_list:
            save.save()
        pass

    exist_media_dirs = get_db_dirs()
    for src_db in src_dbs():
        # ypath.path_res(src_dir)
        ypath.ergodic_folder(media_root(src_db.path), folder_call_back=folder_call)
    return exist_media_dirs


# 删除本地不存在的数据
def handle_meida_db_exists():
    posix_file_list = []
    for dir in src_dbs():
        posix_file_list.extend(
            [ypath.convert_path(file.as_posix()) for file in Path(media_root(dir.path)).rglob('*.*')])
    all_media_set = Media.objects.all()
    with transaction.atomic():
        for media_db in all_media_set:
            if media_db.abs_path not in posix_file_list:
                media_db.delete()


# 获取到media的数据库字段.(Media,MPath)
def get_media_mpath_db(src_db, file_path: str, mdirs):
    # ypath.convert_path(src.replace(self.src_root, '')),
    # str(file.as_posix()), exist_media_dirs, self.desc_root
    if os.path.isdir(file_path):
        return None
    if not yutils.is_movie(file_path):
        return None
    file_path = ypath.convert_path(file_path)
    media_db_query = Media.objects.filter(abs_path=file_path)
    cur_media_db = None
    if len(media_db_query) > 0:
        cur_media_db = media_db_query[0]
        return cur_media_db
    else:
        # target = ypath.decompose_path(
        #     file, str(src_root), str(convert_root), exten='.mp4')
        media_db = Media()
        if (os.path.dirname(file_path) in mdirs):
            media_db.src_dir = mdirs[os.path.dirname(file_path)]  # media_db.src_mpath.dir_id
        else:
            logger.info('该文件没有父文件夹:' + file_path)
            return None
        media_db.abs_path = file_path
        media_db.state = MediaHelp.STATE_INIT
        media_db.file_name = os.path.basename(file_path)
        media_db.src_mpath = src_db
        media_db.desc_path = ypath.del_exten(file_path.replace(media_root(src_db.path), '')) + '.mp4'

        # media_db.nginx_path = target.replace(str(convert_root.as_posix()), '')
        # create_db_list.append(media_db)
        # media_db.folder_key = dm_dict[os.path.dirname(file_path)]
        return media_db


# 转码音频
def analysis_audio_info(media_db: Media, src_db):
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
                    media_db.audio_long_name = audio_stream['codec_long_name']
                    media_db.audio_name = audio_stream['codec_name']
                    digout = True
                    break
        else:
            if len(audio_streams) == 1:
                media_db.audio_long_name = audio_streams[0]['codec_long_name']
                media_db.audio_name = audio_streams[0]['codec_name']
            logger.info('该视频音轨只有一个,不需要转换:' + media_db.abs_path)
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
            return

        if not digout:
            if len(audio_streams) >= 1:
                media_db.audio_long_name = audio_streams[0]['codec_long_name']
                media_db.audio_name = audio_streams[0]['codec_name']
            # media_db.audio_long_name = stream_item['codec_long_name']
            # media_db.audio_name = stream_item['codec_name']
            for audio_stream in audio_streams:
                decode_map += ' -map 0:' + str(audio_stream['index'])
            #     out_content += str(index) + ':' + str(audio_stream) + '\n'
            #     index += 1
            # select_audio = len(audio_streams)
            # while len(audio_streams) <= select_audio or select_audio < 0:
            #     select_audio = int(input(out_content + '选择音轨:'))

        with lock:
            mulit_audio_path = ypath.join(MediaPath.src(), mulit_audio_dir)
        desc_mulit_path = ypath.decompose_path(media_db.abs_path, src_db.path, str(mulit_audio_path))

        out_file = desc_mulit_path + '.chi' + ypath.file_exten(media_db.abs_path)
        ypath.create_dirs(desc_mulit_path)
        if os.path.exists(out_file):
            os.remove(out_file)
        logger.info(out_file)
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


# 转码视频
def compress_media(media_db: Media):
    if MediaHelp.is_err(media_db.state):
        return
    if media_db.desc_mpath == None:
        with lock:
            media_db.desc_mpath = MediaPath.pdc().search_by_abs_path(MediaPath.desc(), is_src=False)
        pass
    d_abs_path = desc_path(media_db)  # ypath.join(media_db.desc_mpath.path, media_db.desc_path)
    # 如果开关开着. 则不管desc是否已有.,根据数据库去覆盖.
    if media_db.state < MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
        # 标记为 未转码完毕
        if os.path.exists(d_abs_path):
            if Globals.MEDIA_SERVICE_COVER_DESC:
                os.remove(d_abs_path)
            else:
                logger.info('MediaService.target exists   所以直接修改数据')
                modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)
    else:
        if not os.path.exists(d_abs_path):  # 状态是转码完毕后. 但是desc文件不存在. 则需要重新转码
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
    if media_db.state >= MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
        logger.info('该文件已经转码过了:' + media_db.abs_path)
        return
    if os.path.exists(d_abs_path):
        os.remove(d_abs_path)
    ypath.create_dirs(d_abs_path)
    # media_db.nginx_path = target
    if media_db.codec_type == 'h264':
        logger.info('这个视频是 h264流视频, 可以直接复制' + media_db.abs_path)
        can_audio_copy = (media_db.audio_name == 'aac' or media_db.audio_name == 'mp3')
        if not can_audio_copy:
            EmailUtil.send('该文件需要检查audio:' + media_db.abs_path + ' \nmedia_db.audio_name:' + media_db.audio_name)
            input('该文件需要检查audio:' + media_db.abs_path)
        if media_db.abs_path.endswith('.mp4') and can_audio_copy:
            os.symlink(media_db.abs_path, d_abs_path)
        else:
            # 这里进行复制内容
            audio_cmd = '-acodec copy' if can_audio_copy else '-acodec aac'
            # audio_cmd = '-acodec copy'
            yutils.process_cmd(
                ffmpeg_tools + ' -i \"' + media_db.abs_path + '\" -vcodec copy ' + audio_cmd + ' \"' + d_abs_path + '\"')

    else:
        # '\"%s\" -i \"%s\"  \"%s\"' % (ffmpeg_tools, src_path, target)
        logger.info('这个视频不是:' + media_db.abs_path)
        yutils.process_cmd('\"%s\" -i \"%s\"  \"%s\"' % (ffmpeg_tools, media_db.abs_path, d_abs_path))
    if not os.path.exists(d_abs_path):
        logger.error('源文件错误:%s' % d_abs_path)
        modify_state(media_db, MediaHelp.STATE_SRC_ERROR)
    else:
        modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)


def create_ts(media_db: Media):
    d_abs_path = ypath.join(media_db.desc_mpath.path, media_db.desc_path)
    print(d_abs_path)


# 生成缩略图
def create_thum(media_db: Media):
    if MediaHelp.is_err(media_db.state):
        return
    desc_root = media_db.desc_mpath.path
    media_tum_root = ypath.join(desc_root,
                                movie_config.img_info.img_root)  # TmpUtil.desc() / movie_config.img_info.img_root
    # convert_root
    # if media_db.state >= MediaHelp.STATE_VIDEO_THUM:
    #     logger.info('该文件已经转缩略图过了:' + media_db.abs_path)
    #     return
    target_img_dir = ypath.join(media_tum_root, media_db.desc_path)
    target_img_dir = ypath.del_exten(target_img_dir)
    ypath.create_dirs(target_img_dir)
    desc = ypath.join(target_img_dir, movie_config.img_info.img)
    desc_thum = ypath.join(target_img_dir, movie_config.img_info.thum)
    if os.path.exists(desc) and os.path.exists(desc_thum):
        logger.info('该视频不需要做缩略图裁切,因为已有:%s' % desc)
        return
    # 裁切缩略图的比例
    thum_percent = int(movie_config.base_info.thum_w) / int(movie_config.base_info.thum_h)

    max_thum_time = int(movie_config.base_info.max_thum_time)
    min_thum_time = int(movie_config.base_info.min_thum_time)

    ypath.create_dirs(desc)

    r_time = random.randint(min_thum_time if media_db.duration > min_thum_time else 0,
                            max_thum_time if media_db.duration > max_thum_time else media_db.duration)
    d_abs_path = ypath.join(media_root(desc_root), media_db.desc_path)
    cmd = ffmpeg_tools + ' -i \"' + d_abs_path + '\" -y  -vframes 1 -ss  00:00:' + str(
        r_time) + ' -f image2  \"' + desc + '\"'
    yutils.process_cmd(cmd)
    if not os.path.exists(desc):
        return
    img = Image.open(desc)
    w, h = img.size
    crop_img = img.crop(yutils.crop_size(w, h, thum_percent))
    crop_img.save(desc_thum)


def modify_state(media_db, state):
    media_db.state = state
    media_db.save()
