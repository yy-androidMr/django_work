# from utils import ypath
import os

from MryangService.frames.ServiceInterface import s_loop
from Tools.CacheTmpInfo import CacheTmpInfo
from frames import ypath, TmpUtil, yutils
from frames.xml import XMLMedia
from MryangService.utils import logger

movie_config = XMLMedia.get_infos()

FFMPEG_KEY = 'FFMPEG_KEY'
FFPROBE_KEY = 'FFPROBE_KEY'
other_format_dir = 'media_mulit_audio'

src_files = []


def delete(event, directory):
    print(event.src_path, directory)


def create(event, directory):
    src_files.append(event.src_path)


def start():
    # 视频源路径
    src_root = ypath.join(TmpUtil.src(), movie_config[XMLMedia.TAGS.DIR_ROOT])
    # 其他音轨存放处
    movie_otherformat = ypath.join(TmpUtil.src(), other_format_dir)
    # 视频转码目标路径
    convert_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.DIR_ROOT])
    # 转码结束后的切片路径
    m3u8_ts_root = ypath.join(TmpUtil.desc(), movie_config[XMLMedia.TAGS.TS_DIR])
    # TmpUtil.clear_key(FFMPEG_KEY)
    # TmpUtil.clear_key(FFPROBE_KEY)
    ffmpeg_tools = TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
    ffprobe_tools = TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n')

    logger.info('src_root:', src_root, 'convert_root:', convert_root, 'm3u8_ts_root:', m3u8_ts_root)
    item_info_list = []
    cache_tmp_info = CacheTmpInfo()

    for root, dirs, files in os.walk(src_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            src_files.append(ypath.join(root, file))

    s_loop(loop, files=src_files)


def loop(files):
    me = loop
    if len(files) == 0:
        return False
    logger.info("MediaService一个流程:" + str(len(files)) + '   ' + files[0])
    del files[0]
    return True

# del_audio_tags()
# convert_video()
#
# XMLMedia.create_media_item_info_xml(item_info_list)
