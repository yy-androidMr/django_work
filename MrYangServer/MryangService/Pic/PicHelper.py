import os

from MryangService.mpath import MediaPath
from frames import yutils, ypath


# def handle_files_md5(src_file,dir_md5):
#
#     if src_file.path not in dir_md5:
#         # ypath.join(str(desc_middle_root), desc_md5), ypath.join(str(desc_thum_root), desc_md5)
#         dir_md5[src_file.path] = yutils.md5_of_str(src_file.relative)
#         # 需要在这里把所有文件夹给创建出来.不然在多线程创建会造成抢占创建.会崩
#         ypath.create_dirs(ypath.join(self.desc_middle_root, dir_md5[src_file.path]), is_dir=True)
#         ypath.create_dirs(ypath.join(self.desc_thum_root, dir_md5[src_file.path]), is_dir=True)
#         ypath.create_dirs(ypath.join(self.desc_webp_root, dir_md5[src_file.path]), is_dir=True)
#     pass


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
