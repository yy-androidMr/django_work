from utils import ypath

from frames.ServiceInterface import ServiceInterface as si


class MediaService(si):
    def __init__(self):
        from utils import TmpUtil

        # 视频源路径
        # src_root = ypath.join(TmpUtil.src(), movie_config[XMLMovie.TAGS.DIR_ROOT])
        # # 非mp4格式视频存放处
        # movie_otherformat = ypath.join(TmpUtil.src(), other_format_dir)
        # # 视频转码目标路径
        # convert_root = ypath.join(TmpUtil.desc(), movie_config[XMLMovie.TAGS.DIR_ROOT])
        # # 转码结束后的切片路径
        # m3u8_ts_root = ypath.join(TmpUtil.desc(), movie_config[XMLMovie.TAGS.TS_DIR])
        # # TmpUtil.clear_key(FFMPEG_KEY)
        # # TmpUtil.clear_key(FFPROBE_KEY)
        # ffmpeg_tools = TmpUtil.input_note(FFMPEG_KEY, '输入对应的ffmpeg文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
        # ffprobe_tools = TmpUtil.input_note(FFPROBE_KEY, '输入对应的ffprobe文件位置(参照link_gitProj_files.txt下载对应的文件):\n')
        #
        # self.log.info('src_root:', src_root, 'convert_root:', convert_root, 'm3u8_ts_root:', m3u8_ts_root)
        # item_info_list = []
        # cache_tmp_info = CacheTmpInfo()
        # del_audio_tags()
        # convert_video()
        # #
        # XMLMovie.create_movie_item_info_xml(item_info_list)

    def loop(self):
        self.log.info("我开始了")
        self.im_out()
