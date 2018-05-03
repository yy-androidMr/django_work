# coding=utf-8
import hashlib
import platform

import os


def is_mac():
    sys_str = platform.system()
    if (sys_str == "Windows"):
        return False
    return True


def get_md5(file_path):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5


def src2middle():
    src = '../../MrYangServer/static/media/pic/src'
    desc = '../../MrYangServer/static/media/pic/middle'
    # print(os.path.exists(src))

    cmd = 'for i in '+src+'/*.jpg;do jpegoptim -m50 -d ' + desc + ' -p "$i";done'
    os.system(cmd)

if __name__ == '__main__':
    src2middle()
