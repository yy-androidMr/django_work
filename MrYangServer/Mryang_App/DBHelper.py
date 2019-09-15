def end_media_state():
    return MediaHelp.STATE_VIDOE_COMPRESS_FINISH;


class MediaHelp:
    STATE_CREATE = -1
    STATE_INIT = 0
    STATE_AUDIO_FINISH = 1  # 音频状态检查完毕 音频会出现非aac和mp3格式的问题.需要转码
    STATE_VIDOE_COMPRESS_FINISH = 2  # 视频转码完毕.
    STATE_VIDEO_THUM = 3  # 裁切略缩图
    STATE_ERROR = 999  # 错误了!!!
    STATE_SRC_ERROR = 1000  # 源文件错误
    STATE_ERROR_END = 1200  # 错误码的结束为止.

    @staticmethod
    def is_err(num):
        return MediaHelp.STATE_ERROR_END >= num >= MediaHelp.STATE_ERROR

    @staticmethod
    def convert(num):
        if num == MediaHelp.STATE_CREATE:
            return '刚创建'
        if num == MediaHelp.STATE_INIT:
            return '刚初始化完成'
        if num == MediaHelp.STATE_AUDIO_FINISH:
            return '多音轨处理完成'
        if num == MediaHelp.STATE_VIDOE_COMPRESS_FINISH:
            return '视频转码完毕'
        if num == MediaHelp.STATE_VIDEO_THUM:
            return '视频缩略图裁切完毕'


class PicHelp:
    STATE_CREATE = -1
    STATE_INIT = 0
    STATE_FINISH = 1  # 从middle 到thum 创建完毕,被视为finish
    STATE_ERROR = 999

    @staticmethod
    def convert(num):
        if num == PicHelp.STATE_CREATE:
            return '刚创建'
        if num == PicHelp.STATE_INIT:
            return '刚初始化完成'
        if num == PicHelp.STATE_FINISH:
            return '本张图处理完毕'
        if num == PicHelp.STATE_ERROR:
            return '本张图处理有误,请尽快处理.'


class MPathHelp:
    SRC = 1
    DESC = 2
