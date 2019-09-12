import datetime
import os
import shutil
import time
import tracemalloc

import gc
import memory_profiler
import piexif
from PIL import Image, ImageDraw, ImageFont

from MryangService import ServiceHelper
from MryangService.ServiceHelper import TimeWatch
from Mryang_App.DBHelper import PicHelp
from Mryang_App.models import Dir, GalleryInfo, PicInfo
from frames import TmpUtil, ypath, yutils, logger, ThreadingPool
from frames.xml import XMLBase


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
        # if type(other) == str:
        #
        # else:

    pass


def start():
    PicSync()


class PicSync:
    def __init__(self):
        pic_config = XMLBase.list_cfg_infos('pic_info')  # XMLMedia.get_infos()
        self.src_root = TmpUtil.src() / pic_config.dir_root  # 源根目录.
        self.webp_cache_root = TmpUtil.src() / pic_config.webp_cache  # src中.有webp.需要转换成png.然后把该webp放置到这个路径.
        self.desc_root = TmpUtil.desc() / pic_config.dir_root  # 输出根目录
        self.desc_middle_root = self.desc_root / pic_config.middle  # 放置放大图的地方
        self.desc_thum_root = self.desc_root / pic_config.thum  # 放置缩略图的地方
        self.desc_webp_root = self.desc_root / pic_config.webp  # 放置webp的地方
        self.middle_area = int(pic_config.max_pic_size) ** 2
        self.thum_size = int(pic_config.thum_size)
        self.in_sync = False
        self.next_loop_sync = False  # 标记. 下次loop要不要执行syn
        self.file_link_list = []
        self.desc_parent_path = {}
        self.MULIT_THREAD_COUNT = 5  # 多线程转换尺寸.
        self.err_pic = []
        self.watch = TimeWatch('PicService')
        self.start()

    # 输出文件名.而不是路径
    def out_file(self, src_file_name):
        desc_name = yutils.md5_of_str(src_file_name)
        return desc_name

    def convert_webp(self, path_class):
        if yutils.is_webp(path_class.path):
            # 如果是webp需要转换一下.然后把webp文件放到另外目录.
            move_target = ypath.decompose_path(path_class.path, str(self.src_root), str(self.webp_cache_root))
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

    # 生成middle->(0为不带后缀的相对路径.2为后缀. 1为src) 路径映射
    # @memory_profiler.profile
    def create_link_dict(self):
        self.file_link_list.clear()
        ypath.del_none_dir(self.src_root)
        logger.info('[create_link_dict] begin')
        src_file_list = ypath.path_res(self.src_root)
        dir_md5 = {}  # 文件夹的md5列表. 避免反复获取md5
        # 这里先组织一下md5文件
        exist_pic_dirs = {}
        all_pic_dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC)
        for pic_db in all_pic_dirs:
            if pic_db.abs_path not in src_file_list:
                logger.info('该文件夹不存在.删除:' + pic_db.abs_path)
                pic_db.delete()
            else:
                exist_pic_dirs[pic_db.abs_path] = pic_db

        gly_infos = GalleryInfo.objects.all()
        exit_gly_info_list = {}
        for gly_info in gly_infos:
            exit_gly_info_list[gly_info.abs_path] = gly_info
            self.desc_parent_path[gly_info.id] = gly_info.desc_path
        # 先组织文件夹. 同步文件夹数据库
        for src_file in src_file_list:
            if not src_file.is_dir:
                continue
            if src_file.path not in dir_md5:
                # ypath.join(str(desc_middle_root), desc_md5), ypath.join(str(desc_thum_root), desc_md5)
                dir_md5[src_file.path] = yutils.md5_of_str(src_file.relative)
                # 需要在这里把所有文件夹给创建出来.不然在多线程创建会造成抢占创建.会崩
                ypath.create_dirs(ypath.join(self.desc_middle_root, dir_md5[src_file.path]), is_dir=True)
                ypath.create_dirs(ypath.join(self.desc_thum_root, dir_md5[src_file.path]), is_dir=True)
                ypath.create_dirs(ypath.join(self.desc_webp_root, dir_md5[src_file.path]), is_dir=True)
            # 插入dir数据
            if src_file.path not in exist_pic_dirs:
                exist_pic_dirs[src_file.path] = ServiceHelper.create_dir(exist_pic_dirs, src_file, yutils.M_FTYPE_PIC)
            # 插入GralleryInfo数据.
            if src_file.path not in exit_gly_info_list:
                g_info = GalleryInfo()
                g_info.folder_key = exist_pic_dirs[src_file.path]
                g_info.abs_path = exist_pic_dirs[src_file.path].abs_path
                g_info.desc_path = ypath.join(self.desc_middle_root, dir_md5[src_file.path])
                g_info.desc_real_path = dir_md5[src_file.path]
                g_info.save()
                exit_gly_info_list[src_file.path] = g_info
        # 后组织文件
        for src_file in src_file_list:
            if src_file.is_dir:
                continue
            if not yutils.is_gif(src_file.ext) and not yutils.is_photo(src_file.ext):
                if not self.convert_webp(src_file):
                    logger.info('PicService.del_not_exist:这文件既不是图片,又不是webp:' + src_file.path)
                continue
            out_file_name = self.out_file(src_file.relative)
            plc = PicLinkCls(exit_gly_info_list[src_file.parent], src_file, dir_md5[src_file.parent], out_file_name,
                             self.desc_middle_root)
            self.file_link_list.append(plc)
        # 删除文件数据库中没有的数据.
        # delete_pic_info_db()
        self.file_link_list.sort(key=lambda x: x.src_file_md5)
        logger.info('[create_link_dict] end')

    # 删除middle和thum中与src不相同的图.
    # @memory_profiler.profile
    def del_not_exist(self):
        def binary_search(pic_info, max):
            min = 0
            while max >= min:
                mid = (max - min) // 2 + min
                if self.file_link_list[mid].src_file_md5 == pic_info.src_md5 and self.file_link_list[
                    mid].src_path == pic_info.src_abs_path:
                    return mid
                if self.file_link_list[mid].src_file_md5 > pic_info.src_md5:
                    max = mid - 1
                else:
                    min = mid + 1
            return -1

        p_infos = PicInfo.objects.all()
        delete_desc_path_list = []
        self.watch.tag_now('同步数据库与src开始:')
        for p_info in p_infos:
            # 这导致了大量的数据库select操作.
            desc = ypath.join(self.desc_parent_path[p_info.gallery_key_id], p_info.desc_name + p_info.ext)
            local_file_count = len(self.file_link_list)
            cur_index = binary_search(p_info, local_file_count)
            if cur_index < 0 or cur_index > local_file_count:
                print('找到了没有用的db数据,应该删除:' + str(p_info.id))
                delete_desc_path_list.append(desc)
                p_info.delete()
            else:
                if os.path.exists(desc):
                    del self.file_link_list[cur_index]

        self.watch.tag_now('同步数据库与src结束, 消耗时长:')

        self.desc_parent_path.clear()
        if self.desc_middle_root.exists():
            desc_middle_str = str(self.desc_middle_root)
            desc_middle_str_len = len(desc_middle_str)
            for root, dirs, files in os.walk(desc_middle_str):
                for file in files:
                    if not yutils.is_gif(file) and not yutils.is_photo(file):
                        continue
                    desc_middle_file = ypath.join(root, file)
                    if desc_middle_file not in self.file_link_list or desc_middle_file in delete_desc_path_list:
                        if os.path.islink(desc_middle_file):
                            os.remove(desc_middle_file)
                        elif os.path.exists(desc_middle_file):
                            os.remove(desc_middle_file)
                        thum_path = ypath.join(str(self.desc_thum_root), desc_middle_file[desc_middle_str_len:])
                        if os.path.exists(thum_path):
                            os.remove(thum_path)

    # @memory_profiler.profile
    # 开启转换.
    def begin_convert(self):
        create_db_list = []

        # tracemalloc.start(5)

        # 传进切割后的map.进行文件转换.
        # @memory_profiler.profile
        def begin_threads(mulit_file_list):

            def cut_middle2thum(m_img, thum):
                if os.path.exists(thum):
                    return m_img
                w, h = m_img.size
                crop_img = m_img.crop(yutils.crop_size(w, h))  # 保存裁切后的图片
                crop_img.thumbnail((self.thum_size, self.thum_size), Image.ANTIALIAS)
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

            # 转webp
            def convert_webp(m_img, webp, middle_file):
                if os.path.exists(webp):
                    return
                if yutils.is_gif(middle_file):
                    return
                m_img.save(webp)

            # 转middle
            def convert_middle(s_img, link_cls_item):
                desc_abs_path = link_cls_item.desc_abs_path
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
                    os.symlink(link_cls_item.src_path, desc_abs_path)
                    return s_img
                # 压缩尺寸
                w, h = s_img.size
                pic_area = w * h
                if pic_area > self.middle_area:
                    proportion = (self.middle_area / pic_area) ** 0.5
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
                    print('处理这张图:' + s_img.filename)
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

            # gc_count = 0
            for link_item in mulit_file_list:
                pi = PicInfo()
                src_file = link_item.src_path
                pi.gallery_key = link_item.g_info
                pi.src_abs_path = link_item.src_path
                pi.src_md5 = link_item.src_file_md5
                pi.desc_name = link_item.out_file_name
                pi.ext = link_item.ext
                try:
                    src_img = Image.open(src_file)
                    pi.size = os.path.getsize(src_file)
                except:
                    self.err_pic.append(src_file)
                    logger.info('这张图有错误!!!!!!!!!!!!!!!!!!!!!!!:' + src_file)
                    continue
                w, h = src_img.size
                pi.width = w
                pi.height = h
                m_img = convert_middle(src_img, link_item)
                w, h = m_img.size
                pi.m_width = w
                pi.m_height = h
                pi.m_size = os.path.getsize(link_item.desc_abs_path)
                pi.state = PicHelp.STATE_FINISH
                pi.is_gif = yutils.is_gif(link_item.ext)
                # webp_file = ypath.join(desc_webp_root, mulit_file_list[middle_file][0] + '.webp')
                # convert_webp(m_img, webp_file, middle_file)
                thum_file = ypath.join(self.desc_thum_root, link_item.desc_rel_path)
                t_img = cut_middle2thum(m_img, thum_file)
                if m_img is not t_img:
                    del m_img
                    del t_img
                else:
                    del m_img
                create_db_list.append(pi)

        fragment_list = {}
        for index, file in enumerate(self.file_link_list):
            n_ind = index % self.MULIT_THREAD_COUNT
            if n_ind not in fragment_list:
                fragment_list[n_ind] = []
            fragment_list[n_ind].append(file)  # file_link_list[file]
        file_len = len(self.file_link_list)
        print('原始src数据长度:' + str(file_len), '  开启了' + str(self.MULIT_THREAD_COUNT) + '个线程.')
        count = 0
        for k in fragment_list:
            cur_len = len(fragment_list[k])
            count += cur_len
            print('重新组合的count:' + str(cur_len) + '  当前坐标:' + str(k))
        print('重组后的长度:' + str(count))
        if count != file_len:
            raise RuntimeError('错误了.处理后的长度和处理前的不一致.这到底怎么回事?')
        tpool = ThreadingPool.ThreadingPool()
        for k in fragment_list:
            tpool.append(begin_threads, fragment_list[k])
        tpool.start()
        self.watch.tag_now('图片同步结束:')
        # if len(create_db_list) > 0:
        #     PicInfo.objects.bulk_create(create_db_list)

    def start(self):
        logger.info('PicService.开始执行同步!!!!')
        self.err_pic.clear()

        self.watch.print_now_time('开始图片转换服务. 开启时间:')
        self.watch.tag_now(print_it=False)
        # 先去重
        ypath.delrepeat_file(self.src_root)
        self.watch.tag_now('去重操作占用时长:')
        # 生成middle->(thum,src) 路径映射
        logger.info('PicService.create_link_dict begin!')
        self.create_link_dict()
        logger.info('PicService.create_link_dict end!')
        self.watch.tag_now('生成src-middle的link_dict 时长:')

        # 删除src中没有.middle中有的图.
        logger.info('PicService.del_not_exist begin!')
        self.del_not_exist()
        logger.info('PicService.del_not_exist end!')
        self.watch.tag_now('同步src-middle-thum时长:')

        # 正式转换.
        logger.info('PicService.begin_convert begin!')
        self.begin_convert()
        logger.info('PicService.begin_convert end!')
        self.watch.tag_now('转换时长:')
        logger.info('PicService.一个loop走完了.不知道有没有同步完 false 代表同步完了')

# # 重新同步.
# def sync_on_back():
#     global next_loop_sync
#     if next_loop_sync:
#         logger.info('当前状态是等待接下来的同步loop')
#         return {'res': 3, 'res_str': '已经发起过同步请求,请等待服务器自动进入同步状态!'}
#     if not in_sync:
#         logger.info('当前状态是没有在同步,已经设置好数值,等下次loop')
#         next_loop_sync = True
#         return {'res': 1, 'res_str': '发起同步操作成功!'}
#     else:
#         logger.info('正在同步,不会做任何操作')
#         return {'res': 2, 'res_str': '正在同步,不会做任何操作'}
