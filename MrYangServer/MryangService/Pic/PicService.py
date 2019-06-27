import os
import shutil
import sys

import psutil
from PIL import Image

from Mryang_App.models import Dir, PicInfo, GalleryInfo
from frames import TmpUtil, ypath, yutils, logger
from frames.xml import XMLBase

pic_config = XMLBase.list_cfg_infos('pic_info')  # XMLMedia.get_infos()
src_root = TmpUtil.src() / pic_config.dir_root  # 源根目录.
desc_root = TmpUtil.desc() / pic_config.dir_root  # 输出根目录
desc_middle_root = desc_root / pic_config.middle  # 放置放大图的地方
desc_thum_root = desc_root / pic_config.thum  # 放置缩略图的地方
webp_root = TmpUtil.src() / pic_config.webp_cache  # 放置webp源文件的地方.

in_sync = False

src_file_dict = {}


def convert_webp(file_path):
    if yutils.is_webp(file_path):
        # 如果是webp需要转换一下.然后把webp文件放到另外目录.
        move_target = ypath.decompose_path(file_path, str(src_root), str(webp_root))
        convert_target = ypath.del_exten(file_path) + '.png'
        if os.path.exists(move_target):
            os.remove(move_target)
        if os.path.exists(convert_target):
            os.remove(convert_target)
        Image.open(file_path).save(convert_target)
        ypath.create_dirs(move_target)
        shutil.move(file_path, move_target)
        logger.info('完成了一个webp转换%s' % move_target)
        return True
    return False


# 生成文件夹数据库.
def gen_dir():
    str_src = str(src_root.as_posix())
    dir_db_paths = {}
    src_dir_list = ypath.path_res(str_src, parse_file=False)
    # for dir in os.listdir(str_src):
    #     m_file_list = ypath.path_res(ypath.join(str_src, dir), parse_file=False)
    #     m_file_list.sort(key=lambda d: d.level)
    #     all_media_dirs = Dir.objects.filter(tags=dir)
    #     for dir_db in all_media_dirs:
    #         if dir_db.abs_path not in m_file_list:
    #             logger.info('被删除的路径:' + dir_db.abs_path)
    #             dir_db.delete()
    #         else:
    #             dir_db_paths[dir_db.abs_path] = dir_db
    #
    #     for local_dir in m_file_list:
    #         if local_dir.path not in dir_db_paths:
    #             dir_db_paths[local_dir.path] = create_dir(dir_db_paths, local_dir, dir)
    #             logger.info('创建该文件夹:' + str(local_dir))
    return dir_db_paths


# 处理数据库里面不相符的图.
def handle_db():
    pass


# 删除middle和thum中与src不相同的图.
def del_not_exist():
    if not os.path.exists(desc_middle_root):
        logger.info('middle pic not exist!')
        return
    logger.info('[delete_not_exist] begin')
    file_list = ypath.path_res(src_root, parse_dir=False)
    # middle_list = ypath.path_res(desc_middle_root, parse_dir=False)

    for file in file_list:
        if not yutils.is_gif(file.ext) and not yutils.is_photo(file.ext):
            # 按照这里说 是否需要插入数据库. 然后标记error啊
            continue


def handle_src_files():
    src_file_dict.clear()
    file_list = ypath.path_res(src_root, parse_dir=False)
    # sys (file_list)
    pass


def start():
    # gi = GalleryInfo.objects.get(intro='b')
    # for _ in range(100000):
    #     p = PicInfo()
    #     p.gallery_key = gi
    #     p.save()

    global in_sync
    in_sync = True
    # 先去重
    ypath.delrepeat_file(src_root)
    # 再组织文件对应关系
    handle_src_files()
    # 再做文件同步
    del_not_exist()
    # 再做数据库同步
    handle_db()
    curP = psutil.Process(os.getpid())
    print(curP.memory_info())
    # 再产生desc中的middle,thum,webp,需要有个bool删除原有数据
    # 再产生 middle 2  thum ? 这个不能再一个操作里吗?

    # 最后校验middle和thum,要不要校验src?
    pass


def loop():
    curP = psutil.Process(os.getpid())
    print(curP.memory_info())
    return False
