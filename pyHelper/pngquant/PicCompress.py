# coding=utf-8
import hashlib
import platform

import os

import piexif
import shutil
from PIL import Image

media_source = '../../MrYangServer/media_source'
src = media_source + '/pic/src'
middle = media_source + '/pic/middle'
thum = media_source + '/pic/thum'


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


def md5_of_str(src):
    md1 = hashlib.md5()
    md1.update(src.encode("utf-8"))
    return md1.hexdigest()


def src2pc(delete_exist):
    middle_size = (2000, 2000)
    # cmd = 'for i in ' + src + '/*.jpg;do jpegoptim -m50 -d ' + desc + ' -p "$i";done'
    # os.system(cmd)
    for root, dirs, files in os.walk(src):
        for file in files:
            source_path = os.path.join(root, file).replace('\\', '/')
            if not any(str_ in file for str_ in ('.jpeg', '.jpg', 'png')):
                continue
            exten = os.path.splitext(source_path)[1]
            simple_path = source_path[len(src):]
            desc_path = middle + '/' + md5_of_str(os.path.dirname(simple_path))
            rename_path = desc_path + '/' + get_md5(source_path) + exten
            if (not delete_exist) and os.path.exists(rename_path):
                print('文件已存在!' + rename_path)
                continue
            if not os.path.exists(desc_path):
                os.makedirs(desc_path)
            img = Image.open(source_path)
            # 压缩尺寸
            img.thumbnail(middle_size, Image.ANTIALIAS)
            # 处理旋转信息.
            old_exif = piexif.load(img.info["exif"])
            if '0th' in old_exif and piexif.ImageIFD.Orientation in old_exif['0th']:
                orientation = old_exif['0th'][piexif.ImageIFD.Orientation]
                if orientation == 6:
                    img = img.rotate(-90, expand=True)
                if orientation == 3:
                    img = img.rotate(180)
                if orientation == 8:
                    img = img.rotate(90, expand=True)
            exif_bytes = piexif.dump({})
            img.save(rename_path, 'JPEG', exif=exif_bytes)
            print(rename_path)


def middle2thum():
    thum_width = 350
    thum_size = (thum_width, thum_width)
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
            w, h = img.size
            if w > h:
                xoff = int((w - h) / 2)
                region = (xoff, 0, h + xoff, h)
            else:
                yoff = int((h - w) / 2)
                region = (0, yoff, w, w + yoff)

            crop_img = img.crop(region)  # 保存裁切后的图片
            crop_img.thumbnail(thum_size, Image.ANTIALIAS)
            exif_dict = piexif.load(crop_img.info["exif"])
            exif_bytes = piexif.dump(exif_dict)
            # crop_img.save(desc_path, 'JPEG')  # 是否需要压缩质量,具体看情况而定.
            crop_img.save(desc_path, 'JPEG', exif=exif_bytes)  # 是否需要压缩质量,具体看情况而定.
            print(desc_path)


def move_info():
    for root, dirs, files in os.walk(src):
        for file in files:
            if 'info' in file:
                src_path = os.path.join(root, file).replace('\\', '/')
                simple_dir = src_path[len(src):]
                desc_path = thum + '/' + md5_of_str(os.path.dirname(simple_dir)) + '/info'

                shutil.copy(src_path, desc_path)

                # print(source_path)


if __name__ == '__main__':
    src2pc(True)
    middle2thum()
    # move_info()
