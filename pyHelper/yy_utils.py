import hashlib
import os
import platform


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten


def is_same_path(l, r):
    l = l.replace('\\', '/')
    r = r.replace('\\', '/')
    return l == r
