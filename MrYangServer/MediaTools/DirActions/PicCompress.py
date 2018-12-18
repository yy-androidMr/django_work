# coding=utf-8

import os

import piexif
import shutil
from PIL import Image, ImageFile

from frames import yutils, TmpUtil, logger
from frames.xml import XMLBase, XMLGallery

MAX_PIC_SIZE = 3000
PicCompress_src = 'PicCompress_src'
PicCompress_desc = 'PicCompress_desc'

(gif_pic, _) = XMLBase.get_gif_banner()


def middle_out_path(source_path):
    exten = os.path.splitext(source_path)[1]
    simple_path = source_path[len(src):]
    dir = yutils.md5_of_str(os.path.dirname(simple_path))
    desc_path = middle + '/' + dir
    rename_path = desc_path + '/' + yutils.get_md5(source_path) + exten
    return (rename_path, desc_path, dir)


#  从src目录压缩一下.到desc
def src2pc(delete_exist):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    middle_area = MAX_PIC_SIZE * MAX_PIC_SIZE
    # cmd = 'for i in ' + src + '/*.jpg;do jpegoptim -m50 -d ' + desc + ' -p "$i";done'
    # os.system(cmd)
    img_link_dic = {}
    for root, dirs, files in os.walk(src):
        for file in files:
            root = root.replace('\\', '/')
            source_path = os.path.join(root, file).replace('\\', '/')
            (rename_path, desc_path, dir) = middle_out_path(source_path)
            if yutils.is_gif(file):
                shutil.copy(source_path, rename_path)
                value = img_link_dic.get(dir, None)
                if not value:
                    img_link_dic[dir] = root
                continue
            if not yutils.is_photo(file):
                continue
            value = img_link_dic.get(dir, None)
            if not value:
                img_link_dic[dir] = root
            if (not delete_exist) and os.path.exists(rename_path):
                print('文件已存在!' + rename_path)
                continue
            if not os.path.exists(desc_path):
                os.makedirs(desc_path)
            print('源：' + source_path)

            # 直接移动
            if not yutils.is_photo(file):
                continue

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

            print(rename_path)
    return img_link_dic


# 从middle 到缩略图
def middle2thum(delete_exist):
    thum_width = 350
    for root, dirs, files in os.walk(middle):
        for file in files:

            source_path = os.path.join(root, file).replace('\\', '/')
            print(source_path)

            desc_path = thum + source_path[len(middle):]
            if (not delete_exist) and os.path.exists(desc_path):
                print('文件已存在!' + desc_path)
                continue
            dir = os.path.dirname(desc_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
                # gif要走配置
            if yutils.is_gif(file) and os.path.exists(gif_pic):
                # gif_pic
                shutil.copy(gif_pic, desc_path)
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


def delete_thum():
    files = os.listdir(thum)
    for file in files:
        path = os.path.join(thum, file)
        if os.path.isdir(path):
            print(path)
            shutil.rmtree(path)


# 删除多余的middle 和thum
def delete_not_exist():
    if not os.path.exists(middle):
        print('middle not exist!')
        return

    print('[delete_not_exist] begin')
    right_map = {}
    for root, dirs, files in os.walk(src):
        for file in files:
            if not yutils.is_photo(file):
                continue
            source_path = os.path.join(root, file).replace('\\', '/')
            (rename_path, _, _) = middle_out_path(source_path)
            if os.path.exists(rename_path):
                right_map[rename_path] = source_path

    delete_list = []
    for root, dirs, files in os.walk(middle):
        for file in files:
            if not yutils.is_photo(file):
                continue
            source_path = os.path.join(root, file).replace('\\', '/')
            if source_path in right_map:
                pass  # print('' + source_path + "  src:" + right_map[source_path])
            else:
                delete_list.append(source_path)
                # print(source_path)
    print('[delete_not_exist] end')


def init_path(key, intro):
    path = TmpUtil.get(key)
    if path is None:
        while path is None or not os.path.exists(path):
            path = input(intro)
        TmpUtil.set(key, path)
    return path


if __name__ == '__main__':
    src = init_path(PicCompress_src, '请指定照片根目录(例如:E:/media_source/pic),目录下就是图片文件夹:\n')
    desc = init_path(PicCompress_desc, '请指定照片输出目录(例如:E:/media_desc/pic,目录下会创建middle和thum):\n')
    logger.info('初始化成功src:', src, ',desc:', desc)
    middle = os.path.join(desc, 'middle')
    thum = os.path.join(desc, 'thum')
    delete_not_exist()
    link_dic = src2pc(False)
    middle2thum(False)
    XMLGallery.append_ifnot_exist(link_dic)
