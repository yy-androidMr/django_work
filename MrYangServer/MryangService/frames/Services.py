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
from MryangService.pic import PicService as ps
from MryangService.pic import PicConvert
from MryangService import MediaService as ms


def im_out(s_name, s_time=60):
    # 没事做了,睡1分钟在看看有没有事,这个如果service多了是否会造成空跑的影响?这个再说了.
    logger.info("服务搁置:" + s_name)
    time.sleep(s_time)


def proxy_method(ins, method_log):
    print()


if __name__ == '__main__':
    # FileObserver.append_call(ms, '/media/')
    logger.info("服务启动正常,该服务进程id:" + str(os.getpid()))
    # tp = tp()
    # tp.append(FileObserver.start, TmpUtil.src())
    # tp.append(proxy_method, ms, 'MediaService.loop')
    # tp.append(proxy_method, ps, 'PicService.loop')
    PicConvert.start()
    # tp.append(PicConvert.start)
    # tp.append(proxy_method, statewatch, 'statewatch.loop')
    # tp.append(statewatch.start)
    # tp.append(ps().start)
    # tp.start()
