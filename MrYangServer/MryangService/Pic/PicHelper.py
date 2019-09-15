import os
import shutil

import piexif
from PIL import Image, ImageDraw, ImageFont

from MryangService import ServiceHelper
from MryangService.mpath import MediaPath
from Mryang_App.DBHelper import PicHelp
from Mryang_App.models import Dir, MPath, GalleryInfo, PicInfo
from frames import yutils, ypath, logger


# # 转webp
# def convert_webp(m_img, webp, middle_file):
#     if os.path.exists(webp):
#         return
#     if yutils.is_gif(middle_file):
#         return
#     m_img.save(webp)
# 获取需要组织picinfo的路径
def get_handle_path_clz(src_dirs, desc_middle_root, db_glys):
    def file_call(file_list):
        for file in file_list:
            if not yutils.is_gif(file.ext) and not yutils.is_photo(file.ext):
                logger.info('这张不是图片:' + file.path)
                continue

            if file.path not in db_pic_info_dict:
                new_file_dict.append(file)

    new_file_dict = []
    pic_info_query = PicInfo.objects.all()
    db_pic_info_dict = {}
    for pic_info in pic_info_query:
        if pic_info.state == PicHelp.STATE_FINISH:
            db_pic_info_dict[pic_info.src_abs_path] = [pic_info.desc_mpath.dir.abs_path, pic_info]
    for src_dir in src_dirs:
        ypath.ergodic_folder(src_dir, file_call_back=file_call)
    return new_file_dict


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


def begin_threads(mtp):
    for link_item in mtp.f_list:
        if not yutils.is_gif(link_item.ext) and not yutils.is_photo(link_item.ext):
            logger.info('这张不是图片:' + link_item.path)
            continue
        gallery_dir = os.path.dirname(link_item.relative)

        desc_root = MediaPath.desc()
        desc_middle_path = ypath.join(desc_root, mtp.desc_middle_root, mtp.db_glys[gallery_dir].desc_real_path,
                                      link_item.folder_md5 + link_item.ext)
        desc_thum_path = ypath.join(desc_root, mtp.desc_thum_root, mtp.db_glys[gallery_dir].desc_real_path,
                                    link_item.folder_md5 + link_item.ext)
        pi = PicInfo()

        src_file = link_item.path
        pi.gallery_key = mtp.db_glys[gallery_dir]
        pi.src_name = link_item.relative
        pi.desc_name = link_item.folder_md5
        pi.ext = link_item.ext
        pi.src_abs_path = src_file
        pi.src_mpath = mtp.all_mpath_dict[link_item.pic_root]
        try:
            file_steam = open(src_file, 'rb')
            pi.src_md5 = yutils.get_md5_steam(file_steam)
            src_img = Image.open(file_steam)
            pi.size = os.path.getsize(src_file)
        except:
            mtp.err_list.append(src_file)
            logger.info('这张图有错误!!!!!!!!!!!!!!!!!!!!!!!:' + src_file)
            continue
        w, h = src_img.size
        pi.width = w
        pi.height = h
        pi.desc_mpath = mtp.all_mpath_dict[desc_root]
        ypath.create_dirs(desc_middle_path)
        m_img = convert_middle(src_img, link_item.path, desc_middle_path, mtp.middle_area)
        w, h = m_img.size
        pi.m_width = w
        pi.m_height = h
        pi.m_size = os.path.getsize(desc_middle_path)
        pi.state = PicHelp.STATE_FINISH
        pi.is_gif = yutils.is_gif(link_item.ext)
        # webp_file = ypath.join(desc_webp_root, mulit_file_list[middle_file][0] + '.webp')
        # convert_webp(m_img, webp_file, middle_file)

        ypath.create_dirs(desc_thum_path)

        t_img = cut_middle2thum(m_img, desc_thum_path, mtp.thum_size)
        if m_img is not t_img:
            del m_img
            del t_img
        else:
            del m_img
        mtp.create_db_list.append(pi)
    pass


def mpath_dict(type=None, byid=True):
    if type:
        mpath_query = MPath.objects.filter(type=type)
    else:
        mpath_query = MPath.objects.all()
    mpath_cache = {}
    for mpath_db in mpath_query:
        if byid:
            mpath_cache[mpath_db.id] = mpath_db.dir.abs_path
        else:
            mpath_cache[mpath_db.dir.abs_path] = mpath_db

    return mpath_cache


def gallery_dict(byid=True):
    gly_query = GalleryInfo.objects.all()
    gly_dict = {}
    for gly in gly_query:
        if byid:
            gly_dict[gly.id] = gly.desc_real_path
        else:
            gly_dict[gly.desc_real_path] = gly
    return gly_dict


# 生成dir
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


def db_dir_exist(db_dirs, src_dir_list):
    # for pic_db in all_pic_dirs:
    #     if pic_db.abs_path not in src_file_list:  # 这里是不是考虑优化? abs_path的父节点有没有在数据库中.并且文件存在.
    #         logger.info('该文件夹不存在.删除:' + pic_db.abs_path)
    #         pic_db.delete()
    #     else:
    #         exist_pic_dirs[pic_db.abs_path] = pic_db
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


def src_list(src_root):
    src_paths = []
    for src_dir in MediaPath.src_list:
        src_paths.append(ypath.join(src_dir.path, src_root))
    return src_paths


def desc_list(desc_root):
    src_paths = []
    for desc_dir in MediaPath.desc_list:
        src_paths.append(ypath.join(desc_dir.path, desc_root))
    return src_paths


class PicLinkCls:
    def __init__(self, g_info, src, dir_md5, out_file_name, desc_middle_root):
        self.src_path = src.path  # src的绝对路径.
        self.dir_md5 = dir_md5
        self.out_file_name = out_file_name  # 只是输出的名字. 是一个md5不带后缀
        self.ext = src.ext
        self.g_info = g_info
        self.src_base_name = src.name
        self.src_file_md5 = yutils.get_md5(src.path)
        self.desc_rel_path = ypath.join(dir_md5, out_file_name + src.ext)
        self.desc_abs_path = ypath.join(desc_middle_root, self.desc_rel_path)

    def __eq__(self, other):
        return other == self.desc_abs_path
