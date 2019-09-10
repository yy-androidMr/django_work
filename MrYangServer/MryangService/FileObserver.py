import time

from watchdog import events
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# from watchdog.events import
from frames import ypath, TmpUtil

MOVE = 'move'
CREATE = 'create'
DELETE = 'delete'
observer = Observer()


class FileInfo:
    def __init__(self):
        self.tag = ''
        self.src = ''
        self.desc = None

    def modify_tag(self, eve):
        # if self.modify_tag == CREATE and tag == DELETE:
        self.tag = eve.key[0]
        self.src = eve.key[1]
        if hasattr(eve, 'desc_path'):
            self.desc = eve.desc_path

    def __eq__(self, other):
        return self.src == other

    def __repr__(self):
        return '[%s,%s,%s]' % (self.tag, self.src, self.desc)


#
class HandleFileModify:
    def __init__(self):
        self.cache_map = {}

    def append_watch(self, watch_path, e):
        if watch_path not in self.cache_map:
            self.cache_map[watch_path] = []
        try:
            fi = self.cache_map[watch_path][self.cache_map[watch_path].index(e.src_path)]
        except:
            fi = FileInfo()
            self.cache_map[watch_path].append(fi)
        fi.modify_tag(e)

    def __str__(self):
        return str(self.cache_map)


modify_handler = HandleFileModify()


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, watch_path):
        FileSystemEventHandler.__init__(self)
        self.watch_path = watch_path
        # if self.watch_path not in changes_map:
        #     changes_map[self.watch_path] = {}

    def on_moved(self, event):
        modify_handler.append_watch(self.watch_path, event)
        # if event.is_directory:
        #     print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        # else:
        #     print("file moved from {0} to {1} {2}".format(event.src_path, event.dest_path, event.key[2]))
        # if MOVE not in changes_map[self.watch_path]:
        #     changes_map[self.watch_path][MOVE] = []
        # changes_map[self.watch_path][MOVE].append(event.src_path, event.dest_path)

    def on_created(self, event):
        modify_handler.append_watch(self.watch_path, event)

        # if event.is_directory:
        #     print("directory created:{0}".format(event.src_path))
        # else:
        #     print("file created:{0},{1}".format(event.src_path, event.key[2]))
        #
        #     # def key(self):
        #     #     return (self.event_type, self.src_path, self.is_directory)
        # changes_map[self.watch_path][CREATE] = event.src_path

    def on_deleted(self, event):
        modify_handler.append_watch(self.watch_path, event)

        # if event.is_directory:
        #     print("directory deleted:{0}".format(event.src_path))
        # else:
        #     print("file deleted:{0},{1}".format(event.src_path, event.key[2]))
        # if event.src_path not in changes_map[self.watch_path]:
        #     changes_map[self.watch_path][event.src_path] = []
        # changes_map[self.watch_path][DELETE] = event.src_path


def start(*kwg):
    for k in kwg:
        append_path(k)
    observer.start()
    try:
        while True:
            time.sleep(1)
            print(modify_handler)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def append_path(path):
    path = ypath.replace(path)
    handler = FileEventHandler(path)
    observer.schedule(handler, str(path), True)


start(r'D:\cache\res\src\pic')
