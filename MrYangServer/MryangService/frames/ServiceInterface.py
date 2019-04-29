import time
from MryangService.utils import logger, EmailUtil


def s_loop(call, *args, **kws):
    # 无限循环这个loop
    s_name = str(call.__name__)
    logger.info('service启动:' + s_name)
    while True:
        try:
            if call(*args, **kws):
                time.sleep(2)
            else:
                im_out(s_name)
        except Exception as e:
            EmailUtil.send_email('服务有报错,请尽快解决!', repr(e))


def im_out(s_name, s_time=60):
    # 没事做了,睡1分钟在看看有没有事
    logger.info("服务搁置:" + s_name)
    time.sleep(s_time)
