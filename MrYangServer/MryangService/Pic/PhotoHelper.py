import os
import shutil
import time

import piexif
from PIL import Image, ImageDraw, ImageFont
from django.db import transaction

from MryangService import ServiceHelper
from MryangService.mpath import MediaPath
from Mryang_App.DBHelper import PicHelp
from Mryang_App.models import Photo, Dir
from frames import ypath, yutils, logger

SYNC_PHOTO_DB_COUNT = 66 * 10  # 有N个数据.就进行同步,而不是全部组织完毕才同步.这样效率太慢了  66一批?


# key:绝对路径,  value:MPath 数据.
def src_list(src_root):
    src_paths = {}
    for src_dir in MediaPath.mpath_db_cache.src_list:
        src_paths[ypath.join(src_dir.path, src_root)] = src_dir.query
    return src_paths


def desc_list(desc_root):
    desc_paths = {}
    for desc_dir in MediaPath.mpath_db_cache.desc_list:
        desc_paths[ypath.join(desc_dir.path, desc_root)] = desc_dir.query
    return desc_paths


def get_middle_abs_path(id):
    return MediaPath.mpath_db_cache.desc_id_key[id]


# 与文件夹对应, 如果没有文件夹, 删除数据库 Dir
def del_not_exist(middle_dir):
    # 需要验证 还没验证呢
    p_infos = Photo.objects.all()
    with transaction.atomic():
        for p_info in p_infos:
            desc_abs_path = get_middle_abs_path(p_info.desc_mpath_id)
            middle_path = ypath.join(desc_abs_path, middle_dir, p_info.desc_rela_path)
            middle_exist = os.path.exists(middle_path)
            if not os.path.exists(p_info.src_abs_path) or not middle_exist or p_info.state != PicHelp.STATE_FINISH:
                p_info.delete()
                if middle_exist or os.path.islink(middle_path):
                    os.remove(middle_path)


def db_dir_exist(db_dirs, src_dir_list):
    # dir不存在则删除.
    exist_pic_dirs = {}
    for pic_db in db_dirs:
        digout = False
        for src_dir in src_dir_list:
            if src_dir in pic_db.abs_path and os.path.isdir(pic_db.abs_path):
                exist_pic_dirs[pic_db.abs_path] = pic_db
                digout = True
                break
        if not digout:
            pic_db.delete()
    return exist_pic_dirs


def convert_webp(path_class, src_root, webp_cache_root):
    if not yutils.is_gif(path_class.ext) and not yutils.is_photo(path_class.ext) and yutils.is_webp(path_class.path):
        # 如果是webp需要转换一下.然后把webp文件放到另外目录.
        src_root = ypath.join(path_class.pic_root, str(src_root))
        webp_cache_root = ypath.join(path_class.pic_root, str(webp_cache_root))
        move_target = ypath.decompose_path(path_class.path, src_root, webp_cache_root)
        if os.path.exists(move_target):
            os.remove(move_target)
        convert_target = None
        try:
            im = Image.open(path_class.path)
            ext = '.png' if im.format == 'PNG' else '.jpg'
            convert_target = ypath.del_exten(path_class.path) + ext
            if os.path.exists(convert_target):
                os.remove(convert_target)
            im.save(convert_target)
            ypath.create_dirs(move_target)
            shutil.move(path_class.path, move_target)
            path_class.path = convert_target
            return True
        except Exception as e:
            if convert_target and os.path.exists(convert_target):
                os.remove(convert_target)
            pass
        return False
    return False


# 生成dir 删除空文件夹
def create_dirs(src_dirs, src_root, webp_cache_root):
    def get_db_dirs():
        for dir in src_dirs:
            ypath.del_none_dir(dir)
        all_pic_dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC)
        db_dirs = db_dir_exist(all_pic_dirs, src_dirs)
        return db_dirs

    def folder_call(folder_list, is_root):
        if is_root:
            if folder_list.path not in exist_pic_dirs:
                exist_pic_dirs[folder_list.path] = ServiceHelper.create_dir(exist_pic_dirs, folder_list,
                                                                            yutils.M_FTYPE_PIC)
            return
        save_list = []
        for dir in folder_list:
            if dir.path not in exist_pic_dirs:
                db_dir = ServiceHelper.create_dir(exist_pic_dirs, dir,
                                                  yutils.M_FTYPE_PIC, save_it=False)
                exist_pic_dirs[dir.path] = db_dir
                save_list.append(db_dir)
                # PicHelper.handle_files_md5(src_file, dir_md5)
        for save in save_list:
            save.save()
        pass

    def file_call(file_list):
        for file in file_list:
            convert_webp(file, src_root, webp_cache_root)

    exist_pic_dirs = get_db_dirs()
    for src_dir in src_dirs:
        # ypath.path_res(src_dir)
        ypath.ergodic_folder(src_dir, file_call_back=file_call, folder_call_back=folder_call)
    return exist_pic_dirs


# 获取需要组织picinfo的路径
def get_create_dict(src_dirs):
    def file_call(file_list):
        for file in file_list:
            if not yutils.is_gif(file.ext) and not yutils.is_photo(file.ext):
                logger.info('这张不是图片:' + file.path)
                continue

            if file.path not in exist_in_db_list:
                new_file_dict.append(file)

    new_file_dict = []
    pic_info_query = Photo.objects.all()
    exist_in_db_list = []
    for pic_info in pic_info_query:
        if pic_info.state == PicHelp.STATE_FINISH:
            exist_in_db_list.append(pic_info.src_abs_path)
            # db_pic_info_dict[pic_info.src_abs_path] = [pic_info.desc_mpath.dir.abs_path, pic_info]
    for src_dir in src_dirs:
        ypath.ergodic_folder(src_dir, file_call_back=file_call)
    return new_file_dict


# 获取多线程的数据.
def convert_fragment_list(src_dirs, thread_count):
    all_file_list = get_create_dict(src_dirs)
    fragment_list = {}
    for index, file in enumerate(all_file_list):
        n_ind = index % thread_count
        if n_ind not in fragment_list:
            fragment_list[n_ind] = []
        fragment_list[n_ind].append(file)  # file_link_list[file]
    file_len = len(all_file_list)
    print('原始src数据长度:' + str(file_len), '  开启了' + str(thread_count) + '个线程.')
    count = 0
    for k in fragment_list:
        cur_len = len(fragment_list[k])
        count += cur_len
        print('重新组合的count:' + str(cur_len) + '  当前坐标:' + str(k))
    print('重组后的长度:' + str(count))
    if count != file_len:
        raise RuntimeError('错误了.处理后的长度和处理前的不一致.这到底怎么回事?')
    return fragment_list


# 文件输出 middle的相对路径.  2017_10/99
def file_desc_dir(stat, file_path, file_md5):
    if not os.path.exists(file_path):
        return None
    if stat.st_ctime > stat.st_mtime:
        second=int(stat.st_mtime)
    else:
        second=int(stat.st_ctime)
    timeStruct = time.localtime(second)

    # str(int(stat.st_ctime) % 10000) + '_' + pi.src_md5[:5]

    return '%d_%d/%d/%d_%s' % (
        timeStruct.tm_year, timeStruct.tm_mon, second % 100, int(stat.st_ctime) % 10000, file_md5[:5]), stat.st_size


def convert_middle(s_img, src_abs_path, desc_abs_path, middle_area):
    if os.path.exists(desc_abs_path):
        try:
            exist_img = Image.open(desc_abs_path)
            return exist_img
        except:
            os.remove(desc_abs_path)
            pass
    # gif link上
    if yutils.is_gif(desc_abs_path):
        # gif特殊操作.
        os.symlink(src_abs_path, desc_abs_path)
        return s_img
    # 压缩尺寸
    w, h = s_img.size
    pic_area = w * h
    if pic_area > middle_area:
        proportion = (middle_area / pic_area) ** 0.5
        w = int(w * proportion)
        h = int(h * proportion)
    s_img.thumbnail((w, h))
    # 处理旋转信息.
    has_exif = 'exif' in s_img.info
    old_exif = None
    if has_exif:
        pass
        try:
            old_exif = piexif.load(s_img.info["exif"])
            has_exif = True
        except:
            has_exif = False
    if has_exif:
        print('处理这张图:' + src_abs_path)
        if '0th' in old_exif and piexif.ImageIFD.Orientation in old_exif['0th']:
            orientation = old_exif['0th'][piexif.ImageIFD.Orientation]
            if orientation == 6:
                s_img = s_img.rotate(-90, expand=True)
            elif orientation == 3:
                s_img = s_img.rotate(180)
            elif orientation == 8:
                s_img = s_img.rotate(90, expand=True)
        exif_bytes = piexif.dump({})
        s_img.save(desc_abs_path, exif=exif_bytes)
    else:
        pass
        try:
            s_img.save(desc_abs_path)
        except:
            s_img = s_img.convert('RGB')
            s_img.save(desc_abs_path)
    return s_img


def cut_middle2thum(m_img, thum, thum_size):
    if os.path.exists(thum):
        return m_img
    w, h = m_img.size
    crop_img = m_img.crop(yutils.crop_size(w, h))  # 保存裁切后的图片
    crop_img.thumbnail((thum_size, thum_size), Image.ANTIALIAS)
    if yutils.is_gif(thum):
        crop_img = crop_img.convert("RGB")
        draw = ImageDraw.Draw(crop_img)
        font = ImageFont.truetype("arial.ttf", 40, encoding="unic")  # 设置字体
        draw.text((0, 0), u'GIF', font=font)
    try:
        crop_img.save(thum)
    except:
        crop_img = crop_img.convert('RGB')
        crop_img.save(thum)
    return crop_img
