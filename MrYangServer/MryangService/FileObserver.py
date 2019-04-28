import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# from watchdog.events import

call = []


def call_back(method, event):
    for i in call:
        try:
            getattr(i, method)(event, event.is_directory)
        except AttributeError:
            pass


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        # if event.is_directory:
        #     print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        # else:
        #     print("file moved from {0} to {1}".format(event.src_path, event.dest_path))
        call_back('move', event)

    def on_created(self, event):
        # if event.is_directory:
        #     print("directory created:{0}".format(event.src_path))
        # else:
        #     print("file created:{0}".format(event.src_path))
        call_back('create', event)

    def on_deleted(self, event):
        # if event.is_directory:
        #     print("directory deleted:{0}".format(event.src_path))
        # else:
        #     print("file deleted:{0}".format(event.src_path))
        call_back('delete', event)
    # def on_modified(self, event):
    #     if event.is_directory:
    #         print("directory modified:{0}".format(event.src_path))
    #     else:
    #         print("file modified:{0}".format(event.src_path))


def start():
    observer = Observer()
    observer.schedule(FileEventHandler(), r'D:\cache\res\src', True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
