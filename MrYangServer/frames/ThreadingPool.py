# coding=utf-8
import threading


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