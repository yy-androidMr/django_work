import os
import sys
import time

import django
from frames import logger

sys.path.append('./../../')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()

from MryangService.watchdog import statewatch
#
from frames.ThreadingPool import ThreadingPool as tp
from MryangService.Pic import PicService as ps
from MryangService import MediaService as ms


def s_loop(call, call_name, *args, **kws):
    # 无限循环这个loop
    logger.info('service启动:' + call_name)
    while True:
        # try:
        if call(*args, **kws):
            pass
            # time.sleep(0.1)
        else:
            im_out(call_name)
    # except Exception as e:
    #     EmailUtil.send_email('服务有报错,请尽快解决!', repr(e))


def im_out(s_name, s_time=60):
    # 没事做了,睡1分钟在看看有没有事,这个如果service多了是否会造成空跑的影响?这个再说了.
    logger.info("服务搁置:" + s_name)
    time.sleep(s_time)


def proxy_method(ins, method_log):
    ins.start()
    s_loop(ins.loop, method_log)


if __name__ == '__main__':
    # FileObserver.append_call(ms, '/media/')
    logger.info("服务启动正常,该服务进程id:" + str(os.getpid()))
    tp = tp()
    # tp.append(FileObserver.start, TmpUtil.src())
    # tp.append(proxy_method, ms, 'MediaService.loop')
    tp.append(proxy_method, ps, 'PicService.loop')
    tp.append(proxy_method, statewatch, 'statewatch.loop')
    # tp.append(ps().start)
    tp.start()
