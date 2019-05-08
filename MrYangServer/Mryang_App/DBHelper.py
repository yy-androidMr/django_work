def end_media_state():
    return MediaHelp.STATE_VIDOE_COMPRESS_FINISH;


class MediaHelp:
    STATE_CREATE = -1
    STATE_INIT = 0
    STATE_AUDIO_FINISH = 1  # 音频状态检查完毕 音频会出现非aac和mp3格式的问题.需要转码
    STATE_VIDOE_COMPRESS_FINISH = 2  # 视频转码完毕.
    STATE_VIDEO_THUM = 3  # 裁切略缩图

