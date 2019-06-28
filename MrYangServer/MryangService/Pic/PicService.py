import datetime
import os
import shutil
import sys
import time

import math
import piexif
import psutil
from PIL import Image

from Mryang_App.models import Dir, PicInfo, GalleryInfo
from frames import TmpUtil, ypath, yutils, logger, ThreadingPool
from frames.xml import XMLBase

pic_config = XMLBase.list_cfg_infos('pic_info')  # XMLMedia.get_infos()
src_root = TmpUtil.src() / pic_config.dir_root  # 源根目录.
webp_cache_root = TmpUtil.src() / pic_config.webp_cache  # src中.有webp.需要转换成png.然后把该webp放置到这个路径.

desc_root = TmpUtil.desc() / pic_config.dir_root  # 输出根目录
desc_middle_root = desc_root / pic_config.middle  # 放置放大图的地方
desc_thum_root = desc_root / pic_config.thum  # 放置缩略图的地方
desc_webp_root = desc_root / pic_config.webp  # 放置webp的地方
middle_area = int(pic_config.max_pic_size) ** 2

in_sync = False
next_loop_sync = False  # 标记. 下次loop要不要执行syn

desc_file_dict = {}
file_link = {}
MULIT_THREAD_COUNT = 5  # 多线程转换尺寸.
err_pic = []


# 输出文件名.而不是路径
def out_file(src_file_name):
    desc_name = yutils.md5_of_str(src_file_name)
    return desc_name


# 输出文件夹绝对路径.
def out_dir(src_dir):
    desc_md5 = yutils.md5_of_str(src_dir)
    return desc_md5


def convert_webp(path_class):
    if yutils.is_webp(path_class.path):
        # 如果是webp需要转换一下.然后把webp文件放到另外目录.
        move_target = ypath.decompose_path(path_class.path, str(src_root), str(webp_cache_root))
        if os.path.exists(move_target):
            os.remove(move_target)

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
            logger.info('完成了一个webp转换%s' % move_target)
        except Exception:
            logger.info('没有完成webp转换%s' % move_target)
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
    with open('err.txt', 'w+', encoding='utf-8') as f:
        for item in err_pic:
            f.write(item + '\n')
    pass


# 生成middle->(0为不带后缀的相对路径.2为后缀. 1为src) 路径映射
def create_link_dict():
    file_link.clear()
    ypath.del_none_dir(src_root)
    logger.info('[create_link_dict] begin')
    src_file_list = ypath.path_res(src_root)
    dir_md5 = {}  # 文件夹的md5列表. 避免反复获取md5
    # 这里先组织一下md5文件
    for src_file in src_file_list:
        if not src_file.is_dir:
            continue
        if src_file.path not in dir_md5:
            # ypath.join(str(desc_middle_root), desc_md5), ypath.join(str(desc_thum_root), desc_md5)
            dir_md5[src_file.path] = out_dir(src_file.relative)

    for src_file in src_file_list:
        if src_file.is_dir:
            continue
        if not yutils.is_gif(src_file.ext) and not yutils.is_photo(src_file.ext):
            if not convert_webp(src_file):
                logger.info('PicService.del_not_exist:这文件既不是图片,又不是webp:' + src_file.path)
            continue
        out_file_name = out_file(src_file.relative)
        file_link[ypath.join(desc_middle_root, dir_md5[src_file.parent], out_file_name + src_file.ext)] = (
            ypath.join(dir_md5[src_file.parent], out_file_name),
            src_file.path, src_file.ext)
    logger.info('[create_link_dict] end')


# 删除middle和thum中与src不相同的图.
def del_not_exist():
    if desc_middle_root.exists():
        desc_middle_str = str(desc_middle_root)
        desc_middle_str_len = len(desc_middle_str)
        for root, dirs, files in os.walk(desc_middle_str):
            for file in files:
                if not yutils.is_gif(file) and not yutils.is_photo(file):
                    continue
                desc_middle_file = ypath.join(root, file)
                if desc_middle_file not in file_link:
                    if os.path.exists(desc_middle_file):
                        os.remove(desc_middle_file)
                    thum_path = ypath.join(str(desc_thum_root), desc_middle_file[desc_middle_str_len:])
                    if os.path.exists(thum_path):
                        os.remove(thum_path)
    ypath.del_none_dir(desc_root)


# 开启转换.
def begin_convert():
    # 传进切割后的map.进行文件转换.
    def begin_threads(mulit_file_list):
        # 转middle
        def comvert_middle(s_img, file):
            if not os.path.exists(file):
                ypath.create_dirs(file)
                # 压缩尺寸
                w, h = src_img.size
                pic_area = w * h
                if pic_area > middle_area:
                    proportion = (middle_area / pic_area) ** 0.5
                    w = int(w * proportion)
                    h = int(h * proportion)
                s_img.thumbnail((w, h), Image.ANTIALIAS)
                # 处理旋转信息.
                has_exif = 'exif' in s_img.info
                old_exif = None
                if has_exif:
                    try:
                        old_exif = piexif.load(s_img.info["exif"])
                        has_exif = True
                    except:
                        has_exif = False
                if has_exif:
                    print('处理这张图:' + s_img.filename)
                    if '0th' in old_exif and piexif.ImageIFD.Orientation in old_exif['0th']:
                        orientation = old_exif['0th'][piexif.ImageIFD.Orientation]
                        if orientation == 6:
                            s_img = s_img.rotate(-90, expand=True)
                        if orientation == 3:
                            s_img = s_img.rotate(180)
                        if orientation == 8:
                            s_img = s_img.rotate(90, expand=True)
                    exif_bytes = piexif.dump({})
                    s_img.save(file, exif=exif_bytes)
                else:
                    try:
                        s_img.save(file)
                    except:
                        s_img = s_img.convert('RGB')
                        s_img.save(file)

        for middle_file in mulit_file_list:
            ext = mulit_file_list[middle_file][2]
            src_file = mulit_file_list[middle_file][1]
            try:
                src_img = Image.open(src_file)
            except:
                err_pic.append(src_file)
                logger.info('这张图有错误!!!!!!!!!!!!!!!!!!!!!!!:' + src_file)
                continue
            if yutils.is_gif(ext):
                # gif特殊操作.
                continue
            comvert_middle(src_img, middle_file)

            thum_file = ypath.join(desc_thum_root, mulit_file_list[middle_file][0] + ext)
            if not os.path.exists(thum_file):
                pass  # 转thum
            webp_file = ypath.join(desc_webp_root, mulit_file_list[middle_file][0] + '.webp')
            if not os.path.exists(webp_file):  # 只有gif没有webp格式.做一个映射.
                # if im2.mode == 'RGBA':
                pass  # 转webp

        pass

    # file_link
    # MULIT_THREAD_COUNT
    fragment_list = {}

    for index, file in enumerate(file_link):
        n_ind = index % MULIT_THREAD_COUNT
        if n_ind not in fragment_list:
            fragment_list[n_ind] = {}
        fragment_list[n_ind][file] = file_link[file]
    file_len = len(file_link)
    print('原始src数据长度:' + str(file_len), '  开启了' + str(MULIT_THREAD_COUNT) + '个线程.')
    count = 0
    for i in range(MULIT_THREAD_COUNT):
        cur_len = len(fragment_list[i])
        count += cur_len
        print('重新组合的count:' + str(cur_len) + '  当前坐标:' + str(i))
    print('重组后的长度:' + str(count))
    if count != file_len:
        raise RuntimeError('错误了.处理后的长度和处理前的不一致.这到底怎么回事?')
    tpool = ThreadingPool.ThreadingPool()
    for i in range(MULIT_THREAD_COUNT):
        tpool.append(begin_threads, fragment_list[i])
    tpool.start()
    pass


def start():
    global in_sync, next_loop_sync
    in_sync = False
    next_loop_sync = True
    pass


# 重新同步.
def sync_on_back():
    global next_loop_sync
    if next_loop_sync:
        logger.info('当前状态是等待接下来的同步loop')
        return {'res': 3, 'res_str': '已经发起过同步请求,请等待服务器自动进入同步状态!'}
    if not in_sync:
        logger.info('当前状态是没有在同步,已经设置好数值,等下次loop')
        next_loop_sync = True
        return {'res': 1, 'res_str': '发起同步操作成功!'}
    else:
        logger.info('正在同步,不会做任何操作')
        return {'res': 2, 'res_str': '正在同步,不会做任何操作'}


#
def loop():
    global in_sync, next_loop_sync
    # 第二道. 是否做操作强制刷新?
    if not next_loop_sync:
        print('本次不进行同步1')
        return False
    next_loop_sync = False
    # 双重锁, 正在同步则取消.
    if in_sync:
        print('本次也不进行同步2')
        return False
    in_sync = True
    logger.info('PicService.开始执行同步!!!!')
    err_pic.clear()
    # 先去重
    ypath.delrepeat_file(src_root)
    # 生成middle->(thum,src) 路径映射
    logger.info('PicService.create_link_dict begin!')
    create_link_dict()
    logger.info('PicService.create_link_dict end!')
    # 删除src中没有.middle中有的图.
    logger.info('PicService.del_not_exist begin!')
    del_not_exist()
    logger.info('PicService.del_not_exist end!')

    # 正式转换. file_link 结构: [middle文件名]=(thum文件名,src文件名)
    logger.info('PicService.begin_convert begin!')
    begin_convert()
    logger.info('PicService.begin_convert end!')
    # 再产生desc中的middle,thum,webp,需要有个bool删除原有数据
    # 再产生 middle 2  thum ? 这个不能再一个操作里吗?
    # 再做数据库同步
    handle_db()
    # 最后校验middle和thum,要不要校验src?
    logger.info('PicService.一个loop走完了.不知道有没有同步完 false 代表同步完了:' + str(in_sync))
    return False
