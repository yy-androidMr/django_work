# coding:utf-8

# 读取临时文件
import os

import shutil
from pathlib import Path, PurePath

import manage
from frames import yutils

tmpdir = manage.root() / 'tmp'  # os.path.join(manage.project_root(), 'tmp')
res_linkdir = (manage.root() / '../res_link').resolve()
tmpfile = tmpdir / 'tmp_server_cfg'
logdir = tmpdir / 'log'


def create_dirs(file_path, is_dir=False, delete_exist=False):
    if is_dir:
        target_dir = file_path
    else:
        target_dir = os.path.dirname(file_path)

    if target_dir:
        if os.path.exists(target_dir):
            if delete_exist:
                shutil.rmtree(target_dir)
            else:
                return
        os.makedirs(target_dir)


def log_path(name):
    log_file = os.path.join(logdir, name)
    create_dirs(log_file)
    return log_file


def write_tmp(**kwgs):
    create_dirs(tmpfile)
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
        return Path(value)


# 输入记录缓存
def input_path(key, intro):
    path_str = get(key)
    while path_str is None or not os.path.exists(path_str):
        path_str = input(intro)
        set(key, path_str)
    return Path(path_str)  # .replace('\\', '/')


SRC_ROOT_KEY = 'SRC_ROOT_KEY'
DESC_ROOT_KEY = 'DESC_ROOT_KEY'
DESC_TMP_DIR = 'tmp'
src_root = None
desc_root = None


def src():
    global src_root
    while src_root is None or not src_root.exists():
        src_root = input_path(SRC_ROOT_KEY, '请指定资源原始目录(例如:E:/src_root),目录下有个pic文件夹,media文件夹:\n')
        link = res_linkdir / 'src'
        if link.exists():
            os.remove(link)
        os.symlink(src_root, link)
    return src_root


def desc():
    global desc_root
    while desc_root is None or not desc_root.exists():
        desc_root = input_path(DESC_ROOT_KEY, '请指定资源输出目录(例如:E:/desc_root),目录下有什么都行,是原始目录的输出路径:\n')
        link = os.path.join(res_linkdir, 'desc')
        if os.path.exists(link):
            os.remove(link)
        os.symlink(desc_root, link)
    return desc_root


# 输出文件的临时目录.做记录
def desc_tmp():
    tmp = desc() / DESC_TMP_DIR
    create_dirs(tmp, True)
    return tmp

