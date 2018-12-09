import os
import platform
import subprocess

import shutil


def re_exten(path, exten):
    path = os.path.splitext(path)[0]
    return path + exten


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


def process_cmd(cmd, call=None, done_call=None, param=None):
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    cmd_str = []
    while True:
        data = ps.stdout.readline()
        if data == b'':
            if ps.poll() is not None:
                if done_call is not None:
                    done_call(cmd_str, param)
                break
        else:
            line = data.decode('utf-8')
            # print(line, end='')
            cmd_str.append(line.replace('\r\n', ''))
            if call is not None:
                call(line)


def is_mac():
    sys_str = platform.system()
    if (sys_str == "Windows"):
        return False
    return True
