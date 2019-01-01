# coding=utf-8

import os

import piexif
import shutil

import sys
from PIL import Image, ImageFile

from frames import yutils, logger, ypath
from frames.xml import XMLPic

MAX_PIC_SIZE = 3000
thum_width = 350
middle_area = MAX_PIC_SIZE * MAX_PIC_SIZE

# gif占位图
GIF_SPACE = 'gif_space'

pic_cfg = XMLPic.get_infos()

other_file = []


def middle_out_path(source_path, desc_dir=None):
    if not desc_dir:
        desc_dir = middle_out_dir(os.path.dirname(source_path))
    exten = ypath.file_exten(source_path)
    rename_path = ypath.join(desc_dir, yutils.get_md5(source_path) + exten)
    return rename_path, dir


def middle_out_dir(src_dir):
    simple_path = src_dir[len(src):]
    dir = yutils.md5_of_str(simple_path)
    return ypath.join(middle, dir)


# 传进文件夹名称.做多线程处理.
def begin_s2middle_by_threads(src_dir, desc_dir, delete_exist):
    # , source_path, rename_path
    for root, _, files in os.walk(src_dir):
        for file in files:
            source_path = ypath.join(root, file)
            rename_path, _ = middle_out_path(source_path, desc_dir)
            if (not delete_exist) and os.path.exists(rename_path):
                print('文件已存在!' + rename_path)
                continue
            if yutils.is_gif(source_path):
                shutil.copy(source_path, rename_path)
                continue
            if not yutils.is_photo(source_path):
                other_file.append(source_path)
                continue

            yutils.create_dirs(rename_path)
            print('源：' + source_path)

            img = Image.open(source_path)
            # 压缩尺寸
            w, h = img.size
            pic_area = w * h
            if pic_area > middle_area:
                proportion = (middle_area / pic_area) ** 0.5
                w = int(w * proportion)
                h = int(h * proportion)
            img.thumbnail((w, h), Image.ANTIALIAS)
            # 处理旋转信息.
            if 'exif' in img.info:
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
            else:
                try:
                    img.save(rename_path)
                except:
                    img = img.convert('RGB')
                    img.save(rename_path)


# 从src目录压缩一下.到desc
def src2pc(delete_exist):
    if not os.path.exists(src):
        logger.info('src2pc:src not exist!')
        return
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    # cmd = 'for i in ' + src + '/*.jpg;do jpegoptim -m50 -d ' + desc + ' -p "$i";done'
    # os.system(cmd)
    from frames import ThreadingPool
    tpool = ThreadingPool.ThreadingPool()
    img_link_dic = {}
    for root, dirs, files in os.walk(src):
        for dir in dirs:
            src_dir = ypath.join(root, dir)
            out_dir = middle_out_dir(src_dir)
            img_link_dic[out_dir] = src_dir
            tpool.append(begin_s2middle_by_threads, src_dir, out_dir, delete_exist)
    tpool.start()
    print('end mulite thread!!!!!!!!!!!!!!')
    return img_link_dic


# 从middle 到缩略图
def middle2thum(delete_exist):
    if delete_exist and os.path.exists(thum):
        shutil.rmtree(thum)

    for root, dirs, files in os.walk(middle):
        for file in files:

            source_path = ypath.join(root, file)
            print(source_path)

            desc_path = thum + source_path[len(middle):]
            if (not delete_exist) and os.path.exists(desc_path):
                print('文件已存在!' + desc_path)
                continue
            dir = os.path.dirname(desc_path)
            yutils.create_dirs(dir, is_dir=True)
            # gif要走配置
            if yutils.is_gif(file):
                # gif_pic
                shutil.copy(gif_space, desc_path)
                pass
            if not yutils.is_photo(file):
                continue
            img = Image.open(source_path)
            w, h = img.size
            if w > h:
                xoff = int((w - h) / 2)
                region = (xoff, 0, h + xoff, h)
            else:
                yoff = int((h - w) / 2)
                region = (0, yoff, w, w + yoff)

            crop_img = img.crop(region)  # 保存裁切后的图片
            crop_img.thumbnail((thum_width, thum_width), Image.ANTIALIAS)
            if 'exif' in img.info:
                exif_dict = piexif.load(crop_img.info["exif"])
                exif_bytes = piexif.dump(exif_dict)
                # crop_img.save(desc_path, 'JPEG')  # 是否需要压缩质量,具体看情况而定.
                crop_img.save(desc_path, 'JPEG', exif=exif_bytes)  # 是否需要压缩质量,具体看情况而定.
            else:
                try:
                    crop_img.save(desc_path)
                except:
                    crop_img = crop_img.convert('RGB')
                    crop_img.save(desc_path)
            print(desc_path)


# 删除多余的middle 和thum
def delete_not_exist():
    if not os.path.exists(middle):
        logger.info('middle not exist!')
        return

    print('[delete_not_exist] begin')
    right_map = {}
    for root, dirs, files in os.walk(src):
        for file in files:

            if not yutils.is_gif(file) and not yutils.is_photo(file):
                continue
            source_path = ypath.join(root, file)
            (rename_path, _) = middle_out_path(source_path)
            if os.path.exists(rename_path):
                right_map[rename_path] = source_path

    for root, dirs, files in os.walk(middle):
        for file in files:
            if not yutils.is_gif(file) and not yutils.is_photo(file):
                continue
            middle_path = ypath.join(root, file)
            if middle_path in right_map:
                pass  # print('' + source_path + "  src:" + right_map[source_path])
            else:
                thum_path = thum + middle_path[len(middle):]
                if os.path.exists(middle_path):
                    os.remove(middle_path)
                if os.path.exists(thum_path):
                    os.remove(thum_path)
                print('删除文件:', middle_path, thum_path)
    print('[delete_not_exist] end')


if __name__ == '__main__':
    from frames import TmpUtil

    src = TmpUtil.input_path(yutils.RESOURCE_ROOT_KEY,
                             '请指定资源根目录(例如:E:/resource_root),目录下有个%s文件夹,并且%s下就是图片:\n' % (
                                 pic_cfg[XMLPic.TAGS.DIR_ROOT], pic_cfg[XMLPic.TAGS.DIR_ROOT]))
    src = ypath.join(src, pic_cfg[XMLPic.TAGS.DIR_ROOT])
    desc = TmpUtil.input_path(yutils.RESOURCE_DESC_KEY,
                              '请指定资源输出目录(例如:E:/resource_desc_root),目录下会创建%s/middle和%s/thum):\n' % (
                                  pic_cfg[XMLPic.TAGS.DIR_ROOT], pic_cfg[XMLPic.TAGS.DIR_ROOT]))
    desc = ypath.join(desc, pic_cfg[XMLPic.TAGS.DIR_ROOT])

    gif_space = ''
    while not os.path.exists(gif_space):
        gif_space = TmpUtil.input_path(GIF_SPACE,
                                       '请指定gif的占位符的图片位置:\n')

    logger.info('初始化成功src:', src, ',desc:', desc)

    middle = ypath.join(desc, pic_cfg[XMLPic.TAGS.MIDDLE])
    thum = ypath.join(desc, pic_cfg[XMLPic.TAGS.THUM])
    # 去重
    other_file.clear()
    # ypath.delfile(src)
    # delete_not_exist()
    # link_dic = src2pc(False)

    if len(other_file) > 0:
        str = input('警告!发现非图片或gif的文件,请确认:\n').lower()
        if 'y' != str:
            sys.exit(0)
    middle2thum(False)

    # middle_have, thum_have = ypath.compair_path(middle, thum)
    #
    # print(middle_have)
    #
    # if len(middle_have) > 0:
    #     str = input('发现有部分文件没有转换完全,是否继续?(y/n):').lower()
    #     if 'y' != str:
    #         print(middle_have, thum_have)
    #         sys.exit(0)
    #
    # XMLPic.append_ifnot_exist(link_dic)
