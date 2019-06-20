from MryangService.frames import ServiceInterface


def start():
    ServiceInterface.s_loop(loop, 'PicService.loop')


def loop():
    return False

# print(PicService)
