import os
import shutil

from PIL import Image

from MryangService import ServiceHelper
from MryangService.mpath import MediaPath
from Mryang_App.models import Dir, MPath, GalleryInfo
from frames import yutils, ypath


def mpath_dict(type, byid=True):
    mpath_query = MPath.objects.filter(type=type)
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
            gly_dict[gly.desc_real_path] =gly
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
