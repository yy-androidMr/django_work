import os
import platform

media_source = 'MrYangServer/media_source'
static_root = 'MrYangServer/static/media'


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten


def create_dirs(file_path):
    target_dir = os.path.dirname(file_path)
    if target_dir:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)


def is_mac():
    sys_str = platform.system()
    if (sys_str == "Windows"):
        return False
    return True