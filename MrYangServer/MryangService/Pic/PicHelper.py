from MryangService.mpath import MPath
from frames import yutils, ypath


def src_list(src_root):
    src_paths = []
    for src_dir in MPath.src_list:
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
