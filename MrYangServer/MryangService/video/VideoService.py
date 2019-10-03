import os
import threading
from pathlib import Path

from MryangService import ServiceHelper
from MryangService.pic import PhotoHelper
from MryangService.video import VideoHelper
from Mryang_App.DBHelper import MediaHelp
from Mryang_App.models import Dir, Media
from frames import logger, ypath, yutils, TmpUtil
from frames.xml import XMLBase

eve = threading.Event()


# 是否正在同步
def in_sync():
    return eve.isSet()


def sync_on_back():
    if eve.isSet():
        logger.info('正在同步,不会做任何操作')
        # 正在同步了. 不需要修改.
        return {'res': 2, 'res_str': '正在同步,不会做任何操作'}

    logger.info('当前状态是没有在同步,即将唤起线程')
    eve.set()
    return {'res': 1, 'res_str': '发起同步操作成功!'}


def start():
    while True:
        Service().start()
        eve.clear()
        eve.wait()


class Service:
    def __init__(self):
        FFMPEG_KEY = 'FFMPEG_KEY'
        FFPROBE_KEY = 'FFPROBE_KEY'
        movie_config = XMLBase.list_cfg_infos('media_info')  # XMLMedia.get_infos()
        self.desc_root = self.src_root = movie_config.dir_root
        self.ffmpeg_tools = str(TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
        self.ffprobe_tools = str(
            TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n'))
        self.mulit_audio_dir = movie_config.base_info.mulit_audio_dir
        pass

    def start(self):
        self.src_dirs = PhotoHelper.src_list(self.src_root)
        self.desc_dirs = PhotoHelper.desc_list(self.desc_root)
        VideoHelper.handle_meida_db_exists(self.src_dirs)
        dm_dict = VideoHelper.gen_dir(self.src_dirs)
        for src in self.src_dirs:
            media_src_root = Path(src)
            files = media_src_root.rglob('*.*')
            for file in files:
                if not file.is_file() or not yutils.is_movie(file):
                    continue
                media_db, mpath = VideoHelper.get_media_mpath_db(src, str(file.as_posix()), dm_dict)
                VideoHelper.check_media_db_state(media_db)
                if MediaHelp.is_err(media_db.state):
                    media_db.save()
                    continue
                VideoHelper.analysis_audio_info(media_db, self.ffprobe_tools, self.ffmpeg_tools, self.mulit_audio_dir,
                                                mpath)

        # 生成文件夹数据库.
