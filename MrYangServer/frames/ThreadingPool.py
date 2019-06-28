# coding=utf-8
import random
import threading

import time


class ThreadingPool:
    def __init__(self):
        self.threads = []

    def proxy_method(self, method, arg1, arg2):
        method(*arg1, **arg2)

    def append(self, target=None, *keys, **args):
        self.threads.append(threading.Thread(target=self.proxy_method, args=(target, keys, args)))

    def start(self):
        for t in self.threads:
            # t.setDaemon(True)
            t.start()
        for t in self.threads:
            t.join()


# def t(args=None):
#     index = 9
#     print('t is start:' + args)/
#     while index > 0:
#         index = random.randint(0, 2)
#         time.sleep(random.randint(1, 3))
#     print('t is down:' + args)
#
#
# tp = ThreadingPool()
# tp.append(t, args='b')
# tp.append(t, args='2')
# tp.append(t, args='3')
# tp.append(t, args='4')
# tp.append(t, args='5')
# tp.append(t, args='6')
# tp.append(t, args='7')
# tp.append(t, args='8')
# tp.append(t, args='9')
# tp.append(t, args='0')
# tp.append(t, args='11')
# tp.append(t, args='123')
# tp.append(t, args='124')
# tp.append(t, args='125')
# tp.append(t, args='126')
# tp.append(t, args='127')
# tp.append(t, args='128')
# tp.append(t, args='129')
# tp.append(t, args='130')
# tp.append(t, args='131')
# tp.append(t, args='132')
# tp.start()
# print('this finish!!!!!!')
