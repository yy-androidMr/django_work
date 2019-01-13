# coding:utf-8

# 读取临时文件
import os

import shutil
import manage
from frames import yutils, ypath

tmpdir = os.path.join(manage.project_root(), 'tmp')
tmpfile = os.path.join(tmpdir, 'tmp_server_cfg')
logdir = os.path.join(tmpdir, 'log')


def log_path(name):
    log_file = os.path.join(logdir, name)
    ypath.create_dirs(log_file)
    return log_file


def write_tmp(**kwgs):
    ypath.create_dirs(tmpfile)
    with open(tmpfile, 'a+', encoding=yutils.default_encode) as f:
        f.seek(0)
        line = f.readline()
        tmpdict = {}
        if line is not '':
            tmpdict = eval(line)
        tmpdict.update(kwgs)
        line = str(tmpdict)
        f.seek(0)
        f.truncate()
        f.write(line)


def read_tmp():
    if not os.path.exists(tmpfile):
        return {}
    with open(tmpfile, 'r', encoding=yutils.default_encode) as f:
        lines = f.readline()
        if lines is not '':
            return eval(lines)
        return {}


def clear_tmp():
    shutil.rmtree(tmpdir)


def clear_key(*keys):
    if not os.path.exists(tmpfile):
        return
    with open(tmpfile, 'r+', encoding=yutils.default_encode) as f:
        line = f.readline()
        tmpdict = {}
        if line is not '':
            tmpdict = eval(line)

        for key in keys:
            if key in tmpdict:
                tmpdict.pop(key)
                # 存在
        line = str(tmpdict)
        f.seek(0)
        f.truncate()
        f.write(line)


def get(key, default=None):
    tmpdict = read_tmp()
    if key in tmpdict:
        default = tmpdict[key]
    return default


def set(key, value, value_is_path=True):
    if value is str and value_is_path:
        value = value.replace('\\', '/')
    dictarg = {key: value}
    write_tmp(**dictarg)


def input_note(key, intro, ispath=True):
    if ispath:
        return input_path(key, intro)
    else:
        value = get(key)
        while value is None or value is '':
            value = input(intro)
        set(key, value)
        return value


# 输入记录缓存
def input_path(key, intro):
    path = get(key)
    while path is None or not os.path.exists(path):
        path = input(intro)
    set(key, path)
    return path.replace('\\', '/')
