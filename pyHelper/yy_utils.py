import hashlib
import os
import platform

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




