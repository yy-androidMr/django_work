import hashlib
import os
import platform

media_source = 'MrYangServer/media_source'
static_root = 'MrYangServer/static/media'


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten


def create_dirs(file_path, is_dir=False):
    if is_dir:
        target_dir = file_path
    else:
        target_dir = os.path.dirname(file_path)

    if target_dir:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)


def is_mac():
    sys_str = platform.system()
    if (sys_str == "Windows"):
        return False
    return True


def md5_of_str(src):
    md1 = hashlib.md5()
    md1.update(src.encode("utf-8"))
    return md1.hexdigest()
