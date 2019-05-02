import json
import os
import shutil

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()

from MryangService.frames.ServiceInterface import s_loop
from Mryang_App.models import Media, Dir
from Mryang_App.DBHelper import MediaHelp
from frames import ypath, TmpUtil, yutils
from frames.xml import XMLMedia
from MryangService.utils import logger
from django.db import transaction

#  进度校验的key 三个环节.
# STATE_CREATE = -1
# STATE_INIT = 0
# STATE_AUDIO_FINISH = 1  # 音频状态检查完毕
# STATE_VIDOE_COMPRESS_FINISH = 2  # 视频转码完毕.
# --------------------

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'
mulit_audio_dir = 'media_mulit_audio'

movie_config = XMLMedia.get_infos()

ffmpeg_tools = TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
ffprobe_tools = TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
# 视频源路径
media_src_root = ypath.join(TmpUtil.src(), movie_config[XMLMedia.TAGS.DIR_ROOT])
# 其他音轨存放处
mulit_audio_path = ypath.join(TmpUtil.src(), mulit_audio_dir)
# 视频转码目标路径
convert_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.DIR_ROOT])
# 转码结束后的切片路径
m3u8_ts_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.TS_DIR])
# TmpUtil.clear_key(FFMPEG_KEY)
# TmpUtil.clear_key(FFPROBE_KEY)

# logger.info('src_root:', src_root, 'convert_root:', convert_root, 'm3u8_ts_root:', m3u8_ts_root)

src_dbs = []

# create - modified(创建操作over)
# deleted(删除操作over)
# moved - modified(改名字over)
# deleted - created - modifed(文件移动)
# , 'modify_name': [], 'move': []
cache_modify_file = {'create': [], 'delete': []}
cur_file_info = {}


def cur_db():
    return cur_file_info.get('db')


def modify_state(media_db, state):
    media_db.state = state
    media_db.save()


def check_file(path):
    if os.path.isdir(path):
        return False
    if mulit_audio_dir in path:
        return False
    # 如果这里没有该路径. 是不是应该删除?
    if cur_db() and os.path.exists(cur_db().abs_path) and os.path.samefile(
            cur_db().abs_path, path):
        return False
    return True


def move(event, is_directory):
    if is_directory:
        return
    cache_modify_file['delete'].append(event.src_path)
    cache_modify_file['create'].append(event.dest_path)


def delete(event, is_directory):
    if is_directory:
        return
    cache_modify_file['delete'].append(event.src_path)
    # print(event.src_path, directory, 'delete')


def create(event, is_directory):
    if is_directory:
        return
    cache_modify_file['create'].append(event.src_path)


# 讲缓存刷新进去 就是重新组织一下src_dbs列表 :
'''
1.判断文件是否被删除
2.判断文件是否被移动
3.判断文件是否与数据库的一致
4.同步数据库
'''


def flush_cache_file():
    print(cache_modify_file)


def start():
    dm_dict = gen_dir()
    create_db_list = []
    for root, dirs, files in os.walk(media_src_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            if not yutils.is_movie(file):
                continue
            src = ypath.join(root, file)
            try:
                media_db = Media.objects.get(abs_path=src)
                media_db.folder_key = dm_dict[os.path.dirname(src)]
                media_db.save()
            except:
                media_db = Media()
                media_db.abs_path = src
                media_db.state = MediaHelp.STATE_INIT
                media_db.file_name = os.path.basename(src)
                create_db_list.append(media_db)
                media_db.folder_key = dm_dict[os.path.dirname(src)]
            src_dbs.append(media_db)

    # 批量插入
    with transaction.atomic():
        for db in create_db_list:
            db.save()
    # if len(create_db_list) > 0:
    #     Media.objects.bulk_create(create_db_list)
    s_loop(loop)


def loop():
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
    # Media.objects.get()
    # if len(query_set) == 0:


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
        _, desc_mulit_path = ypath.decompose_path(media_db.abs_path, media_src_root, mulit_audio_path)
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


def compress_media(media_db):
    # def update_db(_, desc):
    #     if os.path.exists(media_db.abs_path):
    #         os.remove(media_db.abs_path)
    #     media_db.abs_path = desc
    #     media_db.file_name = os.path.basename(desc)
    #     modify_state(media_db, STATE_VIDOE_COMPRESS_FINISH)

    if media_db.state >= MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
        logger.info('该文件已经转码过了:' + media_db.abs_path)
        return

    (_, target) = ypath.decompose_path(
        media_db.abs_path, media_src_root, convert_root, exten='.mp4')
    ypath.create_dirs(target)
    if os.path.exists(target):
        os.remove(target)
    media_db.desc_path = target
    media_db.nginx_path = target.replace(convert_root, '')
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


def gen_dir():
    def create_dir(path, info, tags):
        name = info[ypath.KEYS.NAME]
        parent_path = info[ypath.KEYS.PARENT]
        rel_path = info[ypath.KEYS.REL]
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

    Dir.objects.filter(type=yutils.M_FTYPE_MOIVE).delete()
    dirs = os.listdir(media_src_root)
    dm_list = {}
    for dir in dirs:
        dict = ypath.path_result(media_src_root, dir, parse_file=False)
        list = sorted(dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])

        for item in list:
            dm_list[item[0]] = create_dir(item[0], item[1], dir)
    return dm_list
