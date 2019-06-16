import time
from MryangService.utils import logger


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
    # 没事做了,睡1分钟在看看有没有事
    logger.info("服务搁置:" + s_name)
    time.sleep(s_time)
