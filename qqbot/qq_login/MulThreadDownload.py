# coding:utf-8
import threading, sys
import requests
import time
import os


class MulThreadDownload(threading.Thread):
    def __init__(self, url, startpos, endpos, f, threadIndex, target, args):
        super(MulThreadDownload, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f
        self._threadIndex = threadIndex
        self._target = target
        self._args = args

    def download(self):
        headers = {"Range": "bytes=%s-%s" % (self.startpos, self.endpos)}
        res = requests.get(self.url, headers=headers)
        # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
        # 所以下面是直接write(res.content)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        if self._target:
            self._target(self._threadIndex, self._args)
            # f.close()

    def run(self):
        self.download()


def on_childthread_finish(threadIndex, downloadMe):
    print(downloadMe.__get_info())


class DownloadMe:
    def __init__(self, url):
        self.url = url
        self.info = "[%s] %s / %s"
        self._filename = self.url.split('/')[-1]
        # 线程数
        self._threadnum = 3

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (
            self._filename, 1, self._threadnum)
        return _info

    def download(self):
        start_time = time.time()
        # 获取文件的大小和文件名
        filesize = int(requests.head(self.url).headers['Content-Length'])
        print("%s filesize:%s" % (self._filename, filesize))

        # 信号量，同时只允许3个线程运行
        threading.BoundedSemaphore(self._threadnum)
        # 默认3线程现在，也可以通过传参的方式设置线程数
        step = filesize // self._threadnum
        mtd_list = []
        start = 0
        end = -1

        # 请空并生成文件
        filename = os.path.join('download', self._filename)
        tempf = open(filename, 'w')
        tempf.close()
        # rb+ ，二进制打开，可任意位置读写
        with open(filename, 'rb+') as f:
            fileno = f.fileno()
            # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
            threadindex = 0
            while end < filesize - 1:
                start = end + 1
                end = start + step - 1
                if end > filesize:
                    end = filesize
                # print("start:%s, end:%s"%(start,end))
                # 复制文件句柄
                dup = os.dup(fileno)
                # print(dup)
                # 打开文件
                fd = os.fdopen(dup, 'rb+', -1)
                # print(fd)
                t = MulThreadDownload(self.url, start, end, fd, threadindex, on_childthread_finish, self)
                t.start()
                mtd_list.append(t)
                threadindex += 1

            for i in mtd_list:
                i.join()
        end = time.time()
        sale_time = end - start_time
        speed = (filesize / 1024) / sale_time
        speed = round(speed, 2)
        print('下载 %s 消耗时间 %s秒, 平均速度 %skb/秒' % (filename, round(sale_time, 1), speed))
