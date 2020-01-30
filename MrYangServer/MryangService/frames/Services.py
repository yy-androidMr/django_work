# coding:utf-8
import os
import sys
import time


sys.path.append('./../../')
import django
from frames import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()
from MryangService.watchdog import statewatch
#
from frames.ThreadingPool import ThreadingPool as tp
from MryangService.pic import PhotoService
from MryangService.video import VideoService

# from MryangService import MediaService as ms


def im_out(s_name, s_time=60):
    # 没事做了,睡1分钟在看看有没有事,这个如果service多了是否会造成空跑的影响?这个再说了.
    time.sleep(s_time)


def proxy_method(ins, method_log):
    print()


if __name__ == '__main__':
    # FileObserver.append_call(ms, '/media/')
    logger.info("服务启动正常,该服务进程id:" + str(os.getpid()))
    # tp.append(FileObserver.start, TmpUtil.src())
    # tp.append(proxy_method, ms, 'MediaService.loop')
    # tp.append(proxy_method, ps, 'PicService.loop')
    # ()
    # PhotoService.start()
    # PhotoConvert.start()
    tp = tp()
    tp.append(PhotoService.start)
    tp.append(VideoService.start)
    tp.append(statewatch.start)

    # PicConvert.start()
    # MPath.objects.all().delete()
    # tp.append(PicConvert.start)
    # tp.append(proxy_method, statewatch, 'statewatch.loop')
    # tp.append(ps().start)
    tp.start()
