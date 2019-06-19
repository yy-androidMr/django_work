import os
import sys
import time
#
sys.path.append('./../..')
#
from MryangService.watchdog import statewatch
#
from frames.ThreadingPool import ThreadingPool as tp
from MryangService import MediaService as ms

if __name__ == '__main__':
    # FileObserver.append_call(ms, '/media/')
    print("服务启动正常,该服务进程id:" + str(os.getpid()))
    tp = tp()
    # tp.append(FileObserver.start, TmpUtil.src())
    tp.append(ms.start)
    tp.append(statewatch.start)
    # tp.append(ps().start)
    tp.start()
