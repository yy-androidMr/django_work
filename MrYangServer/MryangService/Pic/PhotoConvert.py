# from MryangService import ServiceHelper
import os

from django.db import transaction

from MryangService import ServiceHelper
from MryangService.Pic import PicHelper
from MryangService.ServiceHelper import TimeWatch
from Mryang_App import DBHelper
from Mryang_App.models import Dir, GalleryInfo, PicInfo, MPath
from frames import ypath, logger, yutils
from frames.xml import XMLBase

convertIns = None


def start():
    global convertIns
    if convertIns is None:
        convertIns = PConvert()
    convertIns.reload()


class PConvert:
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
        self.in_sync = False
        self.next_loop_sync = False  # 标记. 下次loop要不要执行syn
        self.file_link_list = []
        self.desc_parent_path = {}
        self.MULIT_THREAD_COUNT = 5  # 多线程转换尺寸.
        self.err_pic = []
        self.watch = TimeWatch('PhotoConvert')
        # self.watch = TimeWatch('PicService')
        # self.start()

    def reload(self):
        self.src_dirs = PicHelper.src_list(self.src_root)
        self.desc_dirs = PicHelper.desc_list(self.desc_root)
        logger.info('PicService.开始执行同步!!!!')
        self.err_pic.clear()

        self.watch.print_now_time('开始图片转换服务. 开启时间:')
        self.watch.tag_now(print_it=False)
        # 先去重
        ypath.delrepeat_file_list(self.src_dirs)
        self.watch.tag_now('去重操作占用时长:')
        # 数据库和文件同步
        self.del_not_exist()
        logger.info('PhotoConvert.create_dirs begin!')
        db_dirs = PicHelper.create_dirs(self.src_dirs, self.src_root, self.webp_cache_root)
        logger.info('[create_dirs] end')
        # # 删除src中没有.middle中有的图.
        # logger.info('PicService.del_not_exist begin!')
        # self.del_not_exist()
        # logger.info('PicService.del_not_exist end!')
        self.watch.tag_now('同步create_dirs时长:')
        self.create_gly_info()
        #
        # # 正式转换.
        # logger.info('PicService.begin_convert begin!')
        # self.begin_convert()
        # logger.info('PicService.begin_convert end!')
        # self.watch.tag_now('转换时长:')
        # logger.info('PicService.一个loop走完了.不知道有没有同步完 false 代表同步完了')

    # def start(self):
    #     self.reload()
    def del_not_exist(self):
        mpath_cache = PicHelper.mpath_dict(DBHelper.MPathHelp.DESC)
        gly_cache = PicHelper.gallery_dict()
        p_infos = PicInfo.objects.all()
        del_dict = {}
        with transaction.atomic():
            for p_info in p_infos:
                if not os.path.exists(p_info.src_abs_path):
                    p_info.delete()
                    middle = ypath.join(mpath_cache[p_info.desc_mpath_id],
                                        self.desc_middle_root, gly_cache[p_info.gallery_key_id],
                                        p_info.desc_name + p_info.ext)
                    thum = ypath.join(mpath_cache[p_info.desc_mpath_id],
                                      self.desc_thum_root, gly_cache[p_info.gallery_key_id],
                                      p_info.desc_name + p_info.ext)
                    webp = ypath.join(mpath_cache[p_info.desc_mpath_id],
                                      self.desc_webp_root, gly_cache[p_info.gallery_key_id],
                                      p_info.desc_name + p_info.ext)
                    del_dict[middle] = [thum, webp]
                    pass  # 这里需要删除

        for middle_key in del_dict:
            if os.path.islink(middle_key) or os.path.exists(middle_key):
                os.remove(middle_key)
            for del_path in del_dict[middle_key]:
                if os.path.exists(del_path):
                    os.remove(del_path)

    # 创建GalleryInfo 数据
    def create_gly_info(self):
        def folder_call(folder_list, is_root):
            if is_root:
                return
            with transaction.atomic():
                for folder in folder_list:
                    folder_md5 = yutils.md5_of_str(folder.relative)
                    mpath = mpath_cache.get(folder.pic_root)
                    if folder_md5 in gly_cache and mpath:
                        # 更新mpath
                        gly_cache[folder_md5].mulit_path.add(mpath)
                    else:
                        g_info = GalleryInfo()
                        g_info.src_real_path = folder.relative
                        g_info.desc_real_path = folder_md5
                        g_info.save()
                        gly_cache[folder_md5]=g_info
                        if mpath:
                            g_info.mulit_path.add(mpath)

        gly_cache = PicHelper.gallery_dict(False)
        mpath_cache = PicHelper.mpath_dict(DBHelper.MPathHelp.SRC, byid=False)

        for src_dir in self.src_dirs:
            ypath.ergodic_folder(src_dir, folder_call_back=folder_call)

    def begin_convert(self):
        create_db_list = []
