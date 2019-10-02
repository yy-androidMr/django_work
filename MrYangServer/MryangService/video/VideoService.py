import os
import threading

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
        self.gen_dir()
        VideoHelper.handle_meida_db_exists(self.src_dirs)
        # 生成文件夹数据库.

    def gen_dir(self):
        # str_media_src = str(media_src_root.as_posix())
        dir_db_paths = {}
        for src in self.src_dirs:
            if not os.path.exists(src):
                continue
            for dir in os.listdir(src):
                dir = ypath.join(src, dir)
                if not os.path.isdir(dir):
                    continue
                m_file_list = ypath.path_res(dir, parse_file=False)
                all_media_dirs = Dir.objects.filter(abs_path=dir)
                for dir_db in all_media_dirs:
                    if dir_db.abs_path not in m_file_list:
                        logger.info('被删除的路径:' + dir_db.abs_path)
                        dir_db.delete()
                    else:
                        dir_db_paths[dir_db.abs_path] = dir_db

                for local_dir in m_file_list:
                    if local_dir.path not in dir_db_paths:
                        dir_db_paths[local_dir.path] = ServiceHelper.create_dir(dir_db_paths, local_dir,
                                                                                yutils.M_FTYPE_MOIVE,
                                                                                dir)  # create_dir(dir_db_paths, local_dir, dir)
                        logger.info('创建该文件夹:' + str(local_dir))
        return dir_db_paths

    def compress(media_db):
        # 这里要做三步骤调用  1.音轨检查 2.格式转换(或者复制) 3.切片
        if MediaHelp.is_err(media_db.state):
            return
        cur_file_info['db'] = media_db
        analysis_audio_info(media_db)

        compress_media(media_db)
        create_thum(media_db)
        cur_file_info['db'] = None
