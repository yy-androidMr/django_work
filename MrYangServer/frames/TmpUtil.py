# coding:utf-8

# 读取临时文件
import os

import shutil
import tempfile

from frames import yutils

tmpdir = os.path.join(tempfile.gettempdir(), 'yang_server')
tmpfile = os.path.join(tmpdir, 'tmp_server_cfg')
logdir = os.path.join(tmpdir, 'log')


def log_path(name):
    log_file = os.path.join(logdir, name)
    yutils.create_dirs(log_file)
    return log_file


def write_tmp(**kwgs):
    yutils.create_dirs(tmpfile)
    with open(tmpfile, 'r+') as f:
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
    with open(tmpfile, 'r') as f:
        lines = f.readline()
        if lines is not '':
            return eval(lines)
        return {}


def clear_tmp():
    shutil.rmtree(tmpdir)


def clear_key(*keys):
    if not os.path.exists(tmpfile):
        return
    with open(tmpfile, 'r+') as f:
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


if __name__ == '__main__':
    # write_tmp(a='d',c='d',e='f',g='ddd')
    clear_key('a')
    # write_tmp(c='d')
