import threading


class BaseService:
    def __init__(self):
        self.eve = threading.Event()

    # 判断有没有正在同步, true正在同步
    def is_set(self):
        return self.eve.isSet()

    # 调用这个去解锁loop false代表解锁失败. 有东西正在同步
    def set(self):
        if self.is_set():
            return False
        self.eve.set()
        return True
    
    # 需要实现这个. 去做实际事情
    def loop_call(self):
        pass

    def loop(self):
        while True:
            self.loop_call()
            self.eve.clear()
            self.eve.wait()
