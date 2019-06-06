import json
import os
import random
import shutil
import threading

import django
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()

from MryangService.frames import ServiceInterface
from Mryang_App.models import Media, Dir
from Mryang_App.DBHelper import MediaHelp
from frames import ypath, TmpUtil, yutils
from frames.xml import XMLMedia
from MryangService.utils import logger
from django.db import transaction

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'

movie_config = XMLMedia.get_infos()

ffmpeg_tools = str(TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
ffprobe_tools = str(TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
# 视频源路径
media_src_root = TmpUtil.src() / movie_config.dir_root
# 其他音轨存放处
mulit_audio_path = TmpUtil.src() / movie_config.base_info.mulit_audio_dir
# 视频转码目标路径
convert_root = TmpUtil.desc() / movie_config.dir_root
# 转码结束后的切片路径
m3u8_ts_root = TmpUtil.desc() / movie_config.m3u8_info.ts_dir

#  裁切缩略图的比例
thum_percent = int(movie_config.base_info.thum_w) / int(movie_config.base_info.thum_h)

max_thum_time = int(movie_config.base_info.max_thum_time)
min_thum_time = int(movie_config.base_info.min_thum_time)

src_dbs = []

cur_file_info = {}


def cur_state():
    db = cur_file_info.get('db')
    cur_state_info = {}

    # content = '当前媒体服务的状态:\n'
    if db:
        cur_state_info['abs_path'] = db.abs_path
        cur_state_info['state'] = MediaHelp.convert(db.state)
        cur_state_info['more_src'] = {'count': len(src_dbs)}
        # cur_state_info['more_src']['count'] = len(src_dbs)
        items = []
        for src_db in src_dbs:
            item_db_info = {'abs_path': src_db.abs_path, 'state': MediaHelp.convert(src_db.state)}
            items.append(item_db_info)
        cur_state_info['more_src']['items'] = items
        # return json.dumps(cur_state_info)
    # if len(cache_modify_file) > 0:
    #     cur_state_info['modify_file'] = cache_modify_file
    cur_state_info['res'] = 0

    return cur_state_info


def modify_state(media_db, state):
    media_db.state = state
    media_db.save()


def get_media_dbs(files, dm_dict):
    create_db_list = []
    db_list = []
    for file in files:
        if file.is_dir():
            continue
        if not yutils.is_movie(file):
            continue
        posix_file = file.as_posix()
        parent_posix_file = file.parent.as_posix()
        try:
            media_db = Media.objects.get(abs_path=posix_file)
            # media_db.folder_key = dm_dict[parent_posix_file]
            # media_db.save()
        except:
            media_db = Media()
            media_db.abs_path = posix_file
            media_db.state = MediaHelp.STATE_INIT
            media_db.file_name = posix_file
            create_db_list.append(media_db)
            media_db.folder_key = dm_dict[parent_posix_file]
        db_list.append(media_db)
    return create_db_list, db_list


def start():
    dbs = gen_media_dbs()
    src_dbs.extend(dbs)
    ServiceInterface.s_loop(loop)


def gen_media_dbs():
    global sync_control
    sync_control = True
    dm_dict = gen_dir()
    files = media_src_root.rglob('*')
    create_db_list, dbs = get_media_dbs(files, dm_dict)
    # 批量插入
    with transaction.atomic():
        for db in create_db_list:
            db.save()
    sync_control = False
    return dbs


def loop():
    cur_file_info.clear()
    if len(src_dbs) == 0:
        return False
    logger.info("MediaService一个流程:" + str(len(src_dbs)) + '   ' + src_dbs[0].abs_path)
    compress(src_dbs[0])
    del src_dbs[0]
    if len(src_dbs) == 0:
        return False
    return True


def compress(media_db):
    # 这里要做三步骤调用  1.音轨检查 2.格式转换(或者复制) 3.切片
    cur_file_info['db'] = media_db
    analysis_audio_info(media_db)
    compress_media(media_db)
    # create_thum(media_db)


# 转码音频
def analysis_audio_info(media_db):
    def movie_info_res(cmdlist, _):
        if len(cmdlist) <= 0:
            modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)
            return
        jsonbean = json.loads(''.join(cmdlist))

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

        # desc_file = file +
        _, desc_mulit_path = ypath.decompose_path(media_db.abs_path, str(media_src_root), str(mulit_audio_path))
        out_file = desc_mulit_path + '.chi' + ypath.file_exten(media_db.abs_path)
        ypath.create_dirs(desc_mulit_path)
        if os.path.exists(out_file):
            os.remove(out_file)
        logger.info(out_file)

        copy_cmd = ffmpeg_tools + ' -i \"' + media_db.abs_path + '\"' + decode_map + '  -vcodec copy -acodec copy \"' + out_file + '\"'
        yutils.process_cmd(copy_cmd, done_call=rm_on_audio_copy, param=(media_db.abs_path, out_file, desc_mulit_path))

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
def compress_media(media_db):
    (_, target) = ypath.decompose_path(
        media_db.abs_path, str(media_src_root), str(convert_root), exten='.mp4')

    media_db.desc_path = target
    media_db.nginx_path = target.replace(str(convert_root), '')
    if os.path.exists(target):
        if media_db.state < MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
            print('target exists   所以直接修改数据')
            modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)
    else:
        modify_state(media_db, MediaHelp.STATE_AUDIO_FINISH)

    if media_db.state >= MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
        logger.info('该文件已经转码过了:' + media_db.abs_path)
        return
    if os.path.exists(target):
        os.remove(target)

    ypath.create_dirs(target)

    media_db.desc_path = target
    media_db.nginx_path = target.replace(str(convert_root), '')
    # media_db.nginx_path = target
    if media_db.codec_type == 'h264':
        logger.info('这个视频是 h264流视频, 可以直接复制' + media_db.abs_path)
        if media_db.abs_path.endswith('.mp4'):
            os.symlink(media_db.abs_path, target)
            modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)
        else:
            # 这里进行复制内容
            desc = ypath.del_exten(media_db.abs_path) + '.mp4'
            if os.path.exists(desc):
                os.remove(desc)
            yutils.process_cmd(
                ffmpeg_tools + ' -i \"' + media_db.abs_path + '\" -vcodec copy -acodec copy \"' + desc + '\"')
            if os.path.exists(media_db.abs_path):
                os.remove(media_db.abs_path)
            media_db.abs_path = desc
            media_db.file_name = os.path.basename(desc)
            os.symlink(media_db.abs_path, target)
            modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)

    else:
        # '\"%s\" -i \"%s\"  \"%s\"' % (ffmpeg_tools, src_path, target)
        print('这个视频不是:' + media_db.abs_path)
        yutils.process_cmd('\"%s\" -i \"%s\"  \"%s\"' % (ffmpeg_tools, media_db.abs_path, target))
        modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)


# 生成缩略图
def create_thum(media_db):
    if media_db.state >= MediaHelp.STATE_VIDEO_THUM:
        logger.info('该文件已经转缩略图过了:' + media_db.abs_path)
        return
    desc = ypath.join(ypath.del_exten(media_db.desc_path), movie_config.base_info.img)
    desc_thum = ypath.join(ypath.del_exten(media_db.desc_path), movie_config.base_info.thum)
    ypath.create_dirs(desc)

    r_time = random.randint(min_thum_time if media_db.duration > min_thum_time else 0,
                            max_thum_time if media_db.duration > max_thum_time else media_db.duration)
    cmd = ffmpeg_tools + ' -i \"' + media_db.desc_path + '\" -y  -vframes 1 -ss  00:00:' + str(
        r_time) + ' -f image2  \"' + desc + '\"'
    yutils.process_cmd(cmd)
    img = Image.open(desc)
    w, h = img.size
    crop_img = img.crop(yutils.crop_size(w, h, thum_percent))
    crop_img.save(desc_thum)
    pass


# def cut_video():
#     # 假设已经读取了
#     for root, dirs, files in os.walk(convert_root):
#         for file in files:
#             if '.mp4' in file.lower():
#                 # 获取源文件路径
#                 src_path = ypath.join(root, file)
#                 # 拼写输出文件名
#                 rename = yutils.md5_of_str(os.path.basename(src_path)) + movie_config[XMLMedia.TAGS.DIR_EXTEN]
#                 # 获取输出文件路径
#                 (rela_file_name, target_path) = ypath.decompose_path(src_path, convert_root, m3u8_ts_root,
#                                                                      rename=rename)
#                 # 必须要在这添加xml信息. 每次运行都会替换掉原先的配置.
#                 item_info_list.append(item_info(src_path, rela_file_name))
#
#                 if os.path.exists(target_path):
#                     if cache_tmp_info.tmp_info(src_path).get(TMP_CUT_KEY):
#                         # if False:
#                         # 不做处理.重复切片
#                         logger.info('已存在: %s %s' % (src_path, target_path))
#                         return
#                     else:
#                         shutil.rmtree(target_path)
#                 m3u8_file = ypath.join(target_path, movie_config[XMLMedia.TAGS.NAME])
#                 ypath.create_dirs(m3u8_file)
#                 cmd = '\"' + ffmpeg_tools + '\" -i \"' + src_path + \
#                       '\" -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list \"' + \
#                       m3u8_file + '\" -segment_time 10 \"' + target_path + '/%05d.ts\"'
#
#                 yutils.process_cmd(cmd)
#                 cache_tmp_info.write_info(src_path, TMP_CUT_KEY, True)
#                 logger.info('切割完成:' + target_path)


# 获取同步状态
sync_control = False


# 生成文件夹数据库.
def gen_dir():
    def create_dir(path, info, tags):
        name = info.name
        parent_path = info.parent  # info[ypath.KEYS.PARENT]
        rel_path = info.relative
        d_model = Dir()
        d_model.name = name
        d_model.isdir = True
        d_model.abs_path = path
        d_model.rel_path = rel_path
        d_model.type = yutils.M_FTYPE_MOIVE
        d_model.tags = tags  # if info[ypath.KEYS.LEVEL] == 0 else ''
        try:
            parent = Dir.objects.get(abs_path=parent_path)
            d_model.parent_dir = parent
        except Exception as e:
            print('错误,这货没有爸爸的,忽视这个问题:%s:is not found :%s' % (parent_path, e))
            pass
        d_model.save()
        return d_model

    dicts = ypath.path_res(media_src_root, parse_file=False)
    sortedDict = sorted(dicts, key=lambda d: dicts[d].level)
    dir_db_paths = {}
    all_media_dirs = Dir.objects.filter(tags=movie_config.dir_root)
    for dir_db in all_media_dirs:
        if dir_db.abs_path not in sortedDict:
            print('被删除的路径:' + dir_db.abs_path)
            dir_db.delete()
        else:
            dir_db_paths[dir_db.abs_path] = dir_db

    for local_dir in sortedDict:
        if local_dir not in dir_db_paths:
            dir_db_paths[local_dir] = create_dir(local_dir, dicts[local_dir], movie_config.dir_root)
            print('创建该文件夹:' + local_dir)

    return dir_db_paths


def _sync():
    print('开始同步')
    # gen_dir()
    dbs = gen_media_dbs()
    src_dbs.extend(dbs)
    print('同步成功')
    global sync_control
    sync_control = False


def sync_on_back():
    global sync_control
    if not sync_control:
        sync_control = True
        threading.Thread(target=_sync).start()
    return {'res': 0}


def get_state():
    if sync_control:
        return {'res': 1, 'res_str': '正在同步...'}
    return {'res': 1, 'res_str': '没有在同步'}
