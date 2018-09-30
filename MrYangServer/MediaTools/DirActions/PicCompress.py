# coding=utf-8
import hashlib
import platform

import os

import piexif
import shutil
from PIL import Image, ImageFile

from Mryang_App import yutils
from frames.xml import XMLGallery

cd_count = '../' * 3
src = ''.join([cd_count, yutils.media_source, '/pic/src'])
middle = yutils.transform_path(cd_count, yutils.static_media_root, '/pic/middle')
thum = yutils.transform_path(cd_count, yutils.static_media_root, '/pic/thum')
gif_pic = ''.join([cd_count, yutils.static_media_root, '/pic/gif_bannder.png'])  # media_source +


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
    middle_area = 1500 * 1500
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
            # exten = os.path.splitext(source_path)[1]
            # desc_path = middle + '/' + yutils.md5_of_str(os.path.dirname(simple_path))
            # rename_path = desc_path + '/' + yutils.get_md5(source_path) + exten
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


# 移动info文件,这个操作要修改掉.之后改成xml
def move_info():
    for root, dirs, files in os.walk(src):
        for file in files:
            if 'info' in file:
                src_path = os.path.join(root, file).replace('\\', '/')
                # if not os.path.exists(src_path):
                #     continue
                simple_dir = src_path[len(src):]
                desc_path = thum + '/' + yutils.md5_of_str(os.path.dirname(simple_dir)) + '/info'
                print(':'.join([src_path, desc_path, os.path.dirname(simple_dir)]))

                shutil.copy(src_path, desc_path)

                # print(source_path)


def delete_thum():
    files = os.listdir(thum)
    for file in files:
        path = os.path.join(thum, file)
        if os.path.isdir(path):
            print(path)
            shutil.rmtree(path)


# 删除多余的middle 和thum
def delete_not_exist():
    right_map = {}
    for root, dirs, files in os.walk(src):
        for file in files:
            if not yutils.is_photo(file):
                continue
            source_path = os.path.join(root, file).replace('\\', '/')
            (rename_path, _) = middle_out_path(source_path)
            if (os.path.exists(rename_path)):
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
    for path in delete_list:
        os.remove(path)
    yutils.delete_null_dir(middle)
    delete_thum()


def recombination_xml(link_dic):
    XMLGallery.append_ifnot_exist(link_dic)
    # for root, dirs, files in os.walk(middle):
    #     pass


if __name__ == '__main__':
    # delete_not_exist()
    link_dic = src2pc(False)
    # middle2thum(False)
    # move_info()
    recombination_xml(link_dic)

    pass
