import os
import threading
from pathlib import Path

from MryangService.video import VideoHelper
from Mryang_App.DBHelper import MediaHelp
from frames import logger, yutils, Globals
from functools import cmp_to_key

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
        self.mp4_ext = '.mp4'
        pass

    def test_tags(self, exist_media_dirs):
        for dir in exist_media_dirs:
            if exist_media_dirs[dir].parent_dir == None:
                exist_media_dirs[dir].tags = exist_media_dirs[dir].rel_path.replace('/', '')
                exist_media_dirs[dir].save()
    def sort_files(self,rglob_res):
        def cmp_new(x, y):
            if x.suffix == self.mp4_ext:
                if y.suffix == self.mp4_ext:
                    return 0
                return -1
            else:
                if y.suffix == self.mp4_ext:
                    return 1
                else:
                    return 0

        return sorted(rglob_res,key=cmp_to_key(cmp_new))
    def start(self):
        VideoHelper.handle_meida_db_exists()
        exist_media_dirs = VideoHelper.gen_dir()
        if Globals.TEST_MEIDA_DIR_TAGS:
            self.test_tags(exist_media_dirs)

        for src in VideoHelper.src_dbs():
            media_src_root = Path(VideoHelper.media_root(src.path))
            files = media_src_root.rglob('*.*')
            files = self.sort_files(files)
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

        logger.info('VideoService--------------同步结束!')
        # 生成文件夹数据库.
