import os
import threading

from PIL import Image, ImageFile, PngImagePlugin

ImageFile.LOAD_TRUNCATED_IMAGES = True
PngImagePlugin.MAX_TEXT_MEMORY = 1024 * 1024 * 128  # 设置图片容量到128M
from MryangService.ServiceHelper import TimeWatch
from MryangService.mpath import MediaPath
from MryangService.pic import PhotoHelper
from Mryang_App.DBHelper import PicHelp
from Mryang_App.models import Photo
from frames import ypath, logger, ThreadingPool, yutils
from frames.xml import XMLBase

lock = threading.Lock()
eve = threading.Event()

def start():
    while True:
        Service().start()
        eve.clear()
        eve.wait()


def sync_on_back():
    if eve.isSet():
        logger.info('正在同步,不会做任何操作')
        # 正在同步了. 不需要修改.
        return {'res': 2, 'res_str': '正在同步,不会做任何操作'}

    logger.info('当前状态是没有在同步,即将唤起线程')
    eve.set()
    return {'res': 1, 'res_str': '发起同步操作成功!'}


class Service:
    def __init__(self):
        pic_config = XMLBase.list_cfg_infos('pic_info')  # XMLMedia.get_infos()
        self.src_root = pic_config.dir_root  # 源根目录.
        self.webp_cache_root = pic_config.webp_cache  # src中.有webp.需要转换成png.然后把该webp放置到这个路径.
        self.desc_root = pic_config.dir_root  # 输出根目录
        self.desc_middle_root = ypath.join(self.desc_root, pic_config.middle)  # 放置放大图的地方
        self.desc_thum_root = ypath.join(self.desc_root, pic_config.thum)  # 放置缩略图的地方
        self.desc_webp_root = ypath.join(self.desc_root, pic_config.webp)  # 放置webp的地方
        self.middle_area = int(pic_config.max_pic_size) ** 2
        self.thum_size = int(pic_config.thum_size)
        self.MULIT_THREAD_COUNT = 6  # 多线程转换尺寸.
        self.watch = TimeWatch('PhotoService')
        self.err_pic = []
        self.src_dirs = None
        self.desc_dirs = None

    def start(self):
        self.src_dirs = PhotoHelper.src_list(self.src_root)
        self.desc_dirs = PhotoHelper.desc_list(self.desc_root)
        logger.info('PhotoService.开始执行同步!!!!')
        self.err_pic.clear()
        self.watch.print_now_time('开始图片转换服务. 开启时间:')
        self.watch.tag_now(print_it=False)
        ypath.delrepeat_file_list(self.src_dirs, PngImagePlugin.MAX_TEXT_MEMORY)
        self.watch.tag_now('去重操作占用时长:')
        PhotoHelper.del_not_exist(self.desc_middle_root)
        logger.info('PhotoConvert.create_dirs begin!')
        PhotoHelper.create_dirs(self.src_dirs, self.src_root, self.webp_cache_root)
        logger.info('[create_dirs] end')
        logger.info('PhotoService.begin_convert begin!')
        self.begin_convert()
        # logger.info('PhotoService.begin_convert end!')
        # self.watch.tag_now('转换时长:')

    def begin_convert(self):
        fragment_list = PhotoHelper.convert_fragment_list(self.src_dirs, self.MULIT_THREAD_COUNT)
        tpool = ThreadingPool.ThreadingPool()
        create_db_list = []
        error_list = []
        for k in fragment_list:
            tpool.append(self.begin_threads, create_db_list, fragment_list[k], error_list)
        tpool.start()
        if len(create_db_list) > 0:
            Photo.objects.bulk_create(create_db_list)
        self.watch.tag_now('图片同步结束:')

        logger.info('错误图片列表:' + str(error_list))

    # 多线程回调.
    def begin_threads(self, create_db_list: list, f_list, err_list):
        for link_item in f_list:
            if not yutils.is_gif(link_item.ext) and not yutils.is_photo(link_item.ext):
                logger.info('这张不是图片:' + link_item.path)
                continue
            src_file = link_item.path
            if os.stat(src_file).st_size > PngImagePlugin.MAX_TEXT_MEMORY:
                err_list.append(src_file)
                continue
            pi = Photo()
            pi.src_abs_path = src_file
            pi.src_name = link_item.relative
            pi.src_mpath = MediaPath.mpath_db_cache.src_abs_path_key[link_item.pic_root]
            try:
                file_steam = open(src_file, 'rb')
                pi.src_md5 = yutils.get_md5_steam(file_steam)
                desc_rela_name, pi.src_size = PhotoHelper.file_desc_dir(pi.src_abs_path, pi.src_md5)
                src_img = Image.open(file_steam)
                if src_img.mode == 'RGB':
                    pi.desc_rela_path = desc_rela_name + '.jpg'
                else:
                    pi.desc_rela_path = desc_rela_name + link_item.ext
                pi.src_width, pi.src_height = src_img.size
            except:
                err_list.append(src_file)
                logger.info('这张图有错误!!!!!!!!!!!!!!!!!!!!!!!:' + src_file)
                continue
            with lock:
                desc_root = MediaPath.desc()
                pi.desc_mpath = MediaPath.mpath_db_cache.desc_abs_path_key[desc_root]
                desc_middle_path = ypath.join(desc_root, self.desc_middle_root, pi.desc_rela_path)
                desc_thum_path = ypath.join(desc_root, self.desc_thum_root, pi.desc_rela_path)
                desc_webp_path = ypath.join(desc_root, self.desc_webp_root, pi.desc_rela_path)
                ypath.create_dirs(desc_middle_path)
                ypath.create_dirs(desc_thum_path)
                ypath.create_dirs(desc_webp_path)

            m_img = PhotoHelper.convert_middle(src_img, link_item.path, desc_middle_path, self.middle_area)
            w, h = m_img.size
            pi.mid_width = w
            pi.mid_height = h
            pi.mid_size = os.path.getsize(desc_middle_path)
            pi.state = PicHelp.STATE_FINISH
            pi.is_gif = yutils.is_gif(link_item.ext)
            # webp_file = ypath.join(desc_webp_root, mulit_file_list[middle_file][0] + '.webp')
            # convert_webp(m_img, webp_file, middle_file)
            t_img = PhotoHelper.cut_middle2thum(m_img, desc_thum_path, self.thum_size)
            if m_img is not t_img:
                del m_img
                del t_img
            else:
                del m_img
            with lock:
                create_db_list.append(pi)
                if len(create_db_list) >= PhotoHelper.SYNC_PHOTO_DB_COUNT:
                    Photo.objects.bulk_create(create_db_list)
                    create_db_list.clear()