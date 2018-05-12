import os


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten
