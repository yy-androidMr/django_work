import time
from utils import logger


class ServiceInterface:
    def __init__(self):
        self.log = logger

    def start(self):
        # 无限循环这个loop
        logger.info('service启动:' + self.__str__())
        while True:
            logger.info('service执行:' + self.__str__())
            self.loop()
            time.sleep(2)

    def loop(self):
        pass

    def im_out(self, s_time=60):
        # 没事做了,睡1分钟在看看有没有事
        time.sleep(s_time)
