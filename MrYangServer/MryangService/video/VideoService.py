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
        pass

    def start(self):
        VideoHelper.handle_meida_db_exists()
        exist_media_dirs = VideoHelper.gen_dir()
        for src in VideoHelper.src_dbs():
            media_src_root = Path(VideoHelper.media_root(src.path))
            files = media_src_root.rglob('*.*')
            for file in files:
                if not file.is_file() or not yutils.is_movie(file):
                    continue
                media_db = VideoHelper.get_media_mpath_db(src.query, str(file.as_posix()), exist_media_dirs)
                if media_db == None:
                    continue
                VideoHelper.check_media_db_state(media_db)
                if MediaHelp.is_err(media_db.state):
                    media_db.save()
                    continue
                VideoHelper.analysis_audio_info(media_db, src.query)
                VideoHelper.compress_media(media_db)
                # VideoHelper.create_ts(media_db)
                VideoHelper.create_thum(media_db)
                VideoHelper.modify_state(media_db, MediaHelp.STATE_VIDOE_COMPRESS_FINISH)

        logger.info('--------------同步结束!')
        # 生成文件夹数据库.
