# coding=utf-8
import threading
from time import sleep

import multiprocessing


class ThreadingPool:
    def __init__(self, mulit=20):
        self.threads = []
        self.mulit = mulit

    def append(self, target=None, args=()):
        self.threads.append(threading.Thread(target=target, args=args))

    def start(self):
        # count = len(self.threads)
        # page = int(count / self.mulit) + 1
        # index = 0
        # print(page, 'count:', str(len(self.threads)))
        # while index < count:
        #     for i in range(index, index + self.mulit):
        #         print(i)
        for t in self.threads:
            t.setDaemon(True)
            t.start()
        for t in self.threads:
            t.join()

    def m1(self):
        for i in range(4):
            print('m1')
            sleep(4)

    def m2(self):
        for i in range(5):
            print('m1')
            sleep(1)


def tp(str, time):
    for i in range(5):
        print(str + '_progress:' + i)
        sleep(time)


def download(multi_name):
    print('begin download:' + multi_name)
    for i in range(5):
        print('_progress:' + str(i))
        sleep(3)
    # tp = ThreadingPool()
    # for i in range(2):
    #     tp.append(tp, ('in ' + str(i), 3))
    # tp.start()
    print('end download:' + multi_name)

#
# p = [None]*100
# for i in range(3):
#     p[i] = multiprocessing.Process(target=download, args=('multi_' + str(i) + ':'))
#
# p[0].start()
#
# for i in range(3):
#     print(p[i])
#     # p[i].start()
