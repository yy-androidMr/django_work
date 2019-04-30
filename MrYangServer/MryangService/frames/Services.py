import os

from frames import TmpUtil
from frames.ThreadingPool import ThreadingPool as tp
from MryangService import MediaService as ms
# from PicService import PicService as ps
from MryangService import FileObserver

if __name__ == '__main__':
    FileObserver.append_call(ms, '/media/')
    tp = tp()

    tp.append(FileObserver.start, TmpUtil.src())
    tp.append(ms.start)
    # tp.append(ps().start)
    tp.start()
    print("服务启动正常")
