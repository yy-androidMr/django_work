# -*- coding: UTF8 -*-
import time
from pyquery import PyQuery as pq
import sys, os
import json
import requests
from contextlib import closing

BuffSize = 521


class SaveVideo():
    LessonList = []

    def __init__(self):
        pass

    def downloadVideo(self, url):
        '''
        下载视频
        :param url: 下载url路径
        :return: 文件
        '''
        start_time = time.time()
        filename = url.split('/')[-1]
        with closing(requests.get(url, stream=True)) as response:
            chunk_size = 1024 * BuffSize  # 256k
            content_size = int(response.headers['content-length'])
            output = os.path.join('download', filename)
            progress = ProgressBar(filename, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载",
                                   fin_status="下载完成")
            with open(output, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
            end = time.time()
            sale_time = end - start_time
            speed = (content_size / 1024) / sale_time
            speed = round(speed, 2)
            print('下载 %s 消耗时间 %s秒, 平均速度 %skb/秒' % (filename, round(sale_time, 1), speed))


'''
下载进度
'''


class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (
            self.title, self.status, (self.count / self.chunk_size) * BuffSize, self.unit, self.seq,
            (self.total / self.chunk_size) * BuffSize,
            self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        # print('progressing :%s' % self.count, end='')
        print(self.__get_info())


if __name__ == '__main__':
    C = SaveVideo()
    C.downloadVideo('http://sw.bos.baidu.com/sw-search-sp/software/689272248105b/FlashFXP54_5.4.0.3970_Setup.exe')
    sys.exit()
