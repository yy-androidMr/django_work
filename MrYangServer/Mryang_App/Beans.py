# coding:utf-8
import urllib


class VideoBean:
    tag = ''
    dir = ''
    filenamelist = []
    filetype = ''

    def __init__(self):
        print('')

    def init(self, tag, fileurl):
        self.tag = urllib.quote(tag)
        fileurl = fileurl.replace('./static/media', '')
        self.fileurl = urllib.quote(fileurl.replace('\\', '&'))

    # 初始化红楼梦
    def init_hongloumeng(self):
        self.dir = '%E7%BA%A2%E6%A5%BC%E6%A2%A6%E5%B0%8F%E6%88%8F%E9%AA%A8/'
        self.tag = '红楼梦小戏骨'
        self.filenamelist = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
        self.filetype = '.mp4'

    def init_shashoubuleng(self):
        self.dir = '/'
        self.tag = '这个杀手不太冷'
        self.filenamelist = [urllib.quote('[迅雷下载www.XunBo.Cc]这个杀手不太冷加长版BD1280高清中英双字.rmvb'),
                             '[阳光电影www.ygdy8.net].羞羞的铁拳.HD.720p.国语中字.mkv', '[阳光电影www.ygdy8.net].追龙.HD.720p.国语中字.mkv']
        self.filetype = ''

    def count(self):
        return self._filenamelist.count()

    def abspath(self, name):
        return self.dir + name + self.filetype
