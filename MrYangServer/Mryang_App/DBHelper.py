def end_media_state():
    return MediaHelp.STATE_VIDOE_COMPRESS_FINISH;


class MediaHelp:
    STATE_CREATE = -1
    STATE_INIT = 0
    STATE_AUDIO_FINISH = 1  # 音频状态检查完毕
    STATE_VIDOE_COMPRESS_FINISH = 2  # 视频转码完毕.
