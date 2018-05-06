# coding=utf-8
import hashlib
import platform

import os

import piexif
import shutil
from PIL import Image

src = '../../MrYangServer/static/media/pic/src'
middle = '../../MrYangServer/static/media/pic/middle'
thum = '../../MrYangServer/static/media/pic/thum'


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


def src2middle(delete_exist):
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
            print(os.path.dirname(simple_path))
            desc_path = middle + '/' + md5_of_str(os.path.dirname(simple_path))
            rename_path = desc_path + '/' + get_md5(source_path) + exten
            if (not delete_exist) and os.path.exists(rename_path):
                print('文件已存在!' + rename_path)
                continue
            if not os.path.exists(desc_path):
                os.makedirs(desc_path)
            img = Image.open(source_path)

            img.thumbnail(middle_size, Image.ANTIALIAS)
            # print(exif_dict['0th'][piexif.ImageIFD.Orientation])

            old_exif = piexif.load(img.info["exif"])
            orientation = old_exif['0th'][piexif.ImageIFD.Orientation]
            exif_dict = {"0th": {piexif.ImageIFD.Orientation: orientation}}
            exif_bytes = piexif.dump(exif_dict)

            img.save(rename_path, 'JPEG', quality=50, exif=exif_bytes)

            # new_img = Image.open(rename_path)
            # exif_dict = piexif.load(new_img.info["exif"])
            # exif_dict['0th'][piexif.ImageIFD.Orientation] = orientation
            # # print(exif_dict['0th'][piexif.ImageIFD.Orientation])
            #
            # exif_bytes = piexif.dump(exif_dict)
            # new_img.paste(exif=exif_bytes)

            print(rename_path + ' orientation:' + str(orientation))


def middle2thum():
    thum_width = 350
    thum_size = (thum_width, thum_width)

    # img = Image.open(desc)
    for root, dirs, files in os.walk(middle):
        for file in files:
            if not any(str_ in file for str_ in ('.jpeg', '.jpg', 'png')):
                continue
            source_path = os.path.join(root, file).replace('\\', '/')

            desc_path = thum + source_path[len(middle):]
            dir = os.path.dirname(desc_path)
            desc_path = dir + '/' + os.path.splitext(os.path.basename(desc_path))[0] + '.thum'
            if not os.path.exists(dir):
                os.makedirs(dir)

            img = Image.open(source_path)
            w, h = img.size
            # region = (0, 0, w, h)  # xy起点左上角  zw偏移
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
                # thum = '../../MrYangServer/static/media/pic/thum'
                simple_dir = src_path[len(src):]
                desc_path = thum + '/' + md5_of_str(os.path.dirname(simple_dir)) + '/info'

                shutil.copy(src_path, desc_path)

                # print(source_path)


if __name__ == '__main__':
    src2middle(True)
    middle2thum()
    move_info()
