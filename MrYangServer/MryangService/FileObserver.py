import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# from watchdog.events import
from frames import ypath, TmpUtil

call = {}


def append_call(c, *f):
    call[c] = f


# def flash_action

def call_back(method, event):
    p = ypath.replace(event.src_path)
    for c in call:
        try:
            for f in call[c]:
                if f in p:
                    getattr(c, method)(event, event.is_directory)
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
    observer.schedule(FileEventHandler(), str(path), True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
