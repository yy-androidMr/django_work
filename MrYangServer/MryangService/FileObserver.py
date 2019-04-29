import time

from watchdog import events
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# from watchdog.events import

call = []
#  create - modified 这种行为需要等10分钟刷新吧
ACTION = {
    # 文件创建
    events.EVENT_TYPE_CREATED: [events.EVENT_TYPE_CREATED, events.EVENT_TYPE_MODIFIED, events.EVENT_TYPE_MODIFIED],
    # 文件删除
    events.EVENT_TYPE_DELETED: [events.EVENT_TYPE_DELETED],
    # 文件改名
    events.EVENT_TYPE_MOVED: [events.EVENT_TYPE_MOVED, events.EVENT_TYPE_MODIFIED],
    # # 文件移动,从这里移动到那边
    # events.EVENT_TYPE_MODIFIED: [events.EVENT_TYPE_DELETED, events.EVENT_TYPE_CREATED, events.EVENT_TYPE_MODIFIED]
}
action_stack = {}


# def flash_action

def call_back(method, event):
    for i in call:
        try:
            getattr(i, method)(event, event.is_directory)
        except AttributeError:
            pass


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    # create - modified - modified(创建操作over)
    # deleted(删除操作over)
    # moved - modified(改名字over)
    # deleted - created - modifed(文件移动)
    # 这种操作的时候才允许回调.

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1} {2}".format(event.src_path, event.dest_path, event.key[2]))
        call_back('move', event)

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0},{1}".format(event.src_path, event.key[2]))
        call_back('create', event)

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0},{1}".format(event.src_path, event.key[2]))
        call_back('delete', event)

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0},{1}".format(event.src_path, event.key[2]))


def start(path):
    observer = Observer()
    observer.schedule(FileEventHandler(), path, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
