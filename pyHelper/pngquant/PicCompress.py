# coding=utf-8
import hashlib
import platform

import os

from PIL import Image


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
    middle_size = (2000, 2000)
    # cmd = 'for i in ' + src + '/*.jpg;do jpegoptim -m50 -d ' + desc + ' -p "$i";done'
    # os.system(cmd)
    for root, dirs, files in os.walk(src):
        for file in files:
            source_path = os.path.join(root, file).replace('\\', '/')
            if not any(str_ in file for str_ in ('.jpeg', '.jpg', 'png')):
                continue
            desc_path = desc + source_path[len(src):]
            dir = os.path.dirname(desc_path)
            exten = os.path.splitext(desc_path)[1]
            rename_path = dir + '/' + get_md5(source_path) + exten
            if os.path.exists(rename_path):
                print('文件已存在!' + rename_path)
                continue
            if not os.path.exists(dir):
                os.makedirs(dir)
            img = Image.open(source_path)
            img.thumbnail(middle_size, Image.ANTIALIAS)
            img.save(rename_path, "JPEG", quality=50)
            print(rename_path)


def middle2thum():
    middle = '../../MrYangServer/static/media/pic/middle'
    thum = '../../MrYangServer/static/media/pic/thum'
    thum_size = (300, 300)

    # img = Image.open(desc)
    for root, dirs, files in os.walk(middle):
        for file in files:
            if not any(str_ in file for str_ in ('.jpeg', '.jpg', 'png')):
                continue
            source_path = os.path.join(root, file).replace('\\', '/')

            desc_path = thum + source_path[len(middle):]
            dir = os.path.dirname(desc_path)
            if not os.path.exists(dir):
                os.makedirs(dir)

            img = Image.open(source_path)
            img.thumbnail(thum_size, Image.ANTIALIAS)
            img.save(desc_path, 'JPEG', quality=50)

    pass
    # Image.


if __name__ == '__main__':
    # src2middle()
    middle2thum()
