import os

media_source = '../../MrYangServer/media_source'
static_root = '../../MrYangServer/static/media'


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten


def create_dirs(file_path):
    target_dir = os.path.dirname(file_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
