import json
import os
from socket import *
from MryangService import MediaService as ms
from MryangService.ServiceHelper import TimeWatch
from MryangService.Pic import PicService as ps
from frames import logger

host = '127.0.0.1'
port = 12345
buffsize = 2048
ADDR = (host, port)

watch = TimeWatch('statewatch')


def find_path(str):
    try:
        path_tmp = str.split()[1]
        path_tmp = path_tmp[1:]
        if 'favicon.ico' in path_tmp:
            return None
        return path_tmp
    # path = path_tmp.replace('/', '//')
    # return path[0] + ':' + path[1:]
    except:
        return None


def parse_path(path):
    if path is None:
        return '{\"res\":404}'
    # 解析各种路径.
    if 'MediaState' == path:  # 当前的mediaService处理进度
        return json.dumps(ms.cur_state())
    if 'MediaSyncDb' == path:  # 同步media数据库
        return json.dumps(ms.sync_on_back())
    if 'MediaSyncState' == path:  # 查询media数据库同步状态
        return json.dumps(ms.get_state())
    if 'PicSyncDb' == path:  # 同步Pic数据库
        return json.dumps(ps.sync_on_back())
    if 'mem' == path:
        return json.dumps({'当前占用内存(Mb):': watch.cur_mem})

    return '{\"res\":404}'


def start():
    watch.tag_now('开始启动服务器')
    tctime = socket(AF_INET, SOCK_STREAM)
    tctime.bind(ADDR)
    tctime.listen(3)

    while True:
        logger.info('Wait for connection ...')
        tctimeClient, addr = tctime.accept()
        logger.info("Connection from :", str(addr))

        # while True:
        try:
            data = tctimeClient.recv(buffsize).decode()
        except Exception:
            pass
        # if not data:
        #     print('break!!!!!')
        #     break
        res = parse_path(find_path(data))
        tctimeClient.send(res.encode('gbk'))
        tctimeClient.close()

        # time.sleep(1)
