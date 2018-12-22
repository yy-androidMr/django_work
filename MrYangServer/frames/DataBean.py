# coding:utf-8
import os

from frames import yutils


# 照片切片的时候有个MovieInfo二进制化信息存在了本地.文件名为info
class MovieInfo():
    def __init__(self, file):
        self.file = file
        self.name = yutils.file_name(os.path.basename(file))
        self.size = os.path.getsize(file)
        self.show_size = yutils.fileSizeConvert(self.size)
        from moviepy.editor import VideoFileClip
        self.time = VideoFileClip(self.file).duration
        self.show_time = yutils.time_convert(self.time)
