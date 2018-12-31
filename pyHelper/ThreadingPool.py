# coding=utf-8
# import random
import threading
# import time


class ThreadingPool:
    def __init__(self):
        self.threads = []

    def append(self, target=None, args=()):
        self.threads.append(threading.Thread(target=target, args=args))

    def start(self):
        for t in self.threads:
            t.setDaemon(True)
            t.start()
        for t in self.threads:
            t.join()

#
# def t(arg):
#     index = 9
#     print('t is start:' + arg)
#     while index > 0:
#         index = random.randint(0, 2)
#         time.sleep(random.randint(1, 3))
#     print('t is down:' + arg)
#

# tp = ThreadingPool()
# tp.append(t, args='1')
# tp.append(t, args='2')
# tp.append(t, args='3')
# tp.append(t, args='4')
# tp.append(t, args='5')
# tp.start()
# print('this finish!!!!!!')
