import threading

from MryangService.pic import PhotoService
from frames import logger

eve = threading.Event()


def start():
    while True:

        eve.wait()
        # 等待启动
        eve.clear()


def sync_on_back():
    if PhotoService.in_sync():
        return {'res': 3, 'res_str': '图片库正在同步,暂时无法同步照片墙!'}

    if eve.isSet():
        logger.info('正在同步,不会做任何操作')
        # 正在同步了. 不需要修改.
        return {'res': 2, 'res_str': '正在同步,不会做任何操作'}

    logger.info('当前状态是没有在同步,即将唤起线程')
    eve.set()
    return {'res': 1, 'res_str': '发起同步操作成功!'}
