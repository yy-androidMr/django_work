# from MryangService import ServiceHelper
from MryangService.Pic import PicHelper
from MryangService.ServiceHelper import TimeWatch
from Mryang_App.models import Dir, GalleryInfo
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
        logger.info('PicService.开始执行同步!!!!')
        self.err_pic.clear()

        self.watch.print_now_time('开始图片转换服务. 开启时间:')
        self.watch.tag_now(print_it=False)
        # 先去重
        ypath.delrepeat_file_list(self.src_dirs)
        self.watch.tag_now('去重操作占用时长:')
        # 生成middle->(thum,src) 路径映射
        logger.info('PicService.create_link_dict begin!')
        self.create_link_dict()
        # logger.info('PicService.create_link_dict end!')
        # self.watch.tag_now('生成src-middle的link_dict 时长:')
        #
        # # 删除src中没有.middle中有的图.
        # logger.info('PicService.del_not_exist begin!')
        # self.del_not_exist()
        # logger.info('PicService.del_not_exist end!')
        # self.watch.tag_now('同步src-middle-thum时长:')
        #
        # # 正式转换.
        # logger.info('PicService.begin_convert begin!')
        # self.begin_convert()
        # logger.info('PicService.begin_convert end!')
        # self.watch.tag_now('转换时长:')
        # logger.info('PicService.一个loop走完了.不知道有没有同步完 false 代表同步完了')

    # def start(self):
    #     self.reload()

    # 获取数据库中dirs. 并且删除空目录.
    def get_db_dirs(self):
        for dir in self.src_dirs:
            ypath.del_none_dir(dir)
        all_pic_dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC)
        exist_pic_dirs = PicHelper.db_dir_exist(all_pic_dirs, self.src_dirs)
        return exist_pic_dirs

    # 生成middle->(0为不带后缀的相对路径.2为后缀. 1为src) 路径映射
    # @memory_profiler.profile
    def create_link_dict(self):
        def file_call(file_list):
            print(file_list)
            pass

        logger.info('[create_link_dict] begin')
        exist_pic_dirs = self.get_db_dirs()
        # 这里先组织一下md5文件
        for src_dir in self.src_dirs:
            # ypath.path_res(src_dir)
            ypath.ergodic_folder(src_dir, file_call)
        # PicHelper.handle_files_md5()

        # gly_infos = GalleryInfo.objects.all()
        # exit_gly_info_list = {}
        # for gly_info in gly_infos:
        #     exit_gly_info_list[gly_info.abs_path] = gly_info
        #     self.desc_parent_path[gly_info.id] = gly_info.desc_path
        # # 先组织文件夹. 同步文件夹数据库
        # for src_file in src_file_list:  # 这个也需要优化掉.
        #     if not src_file.is_dir:
        #         continue
        #     if src_file.path not in dir_md5:
        #         # ypath.join(str(desc_middle_root), desc_md5), ypath.join(str(desc_thum_root), desc_md5)
        #         dir_md5[src_file.path] = yutils.md5_of_str(src_file.relative)
        #         # 需要在这里把所有文件夹给创建出来.不然在多线程创建会造成抢占创建.会崩
        #         ypath.create_dirs(ypath.join(self.desc_middle_root, dir_md5[src_file.path]), is_dir=True)
        #         ypath.create_dirs(ypath.join(self.desc_thum_root, dir_md5[src_file.path]), is_dir=True)
        #         ypath.create_dirs(ypath.join(self.desc_webp_root, dir_md5[src_file.path]), is_dir=True)
        #     # 插入dir数据
        #     if src_file.path not in exist_pic_dirs:
        #         exist_pic_dirs[src_file.path] = ServiceHelper.create_dir(exist_pic_dirs, src_file, yutils.M_FTYPE_PIC)
        #     # 插入GralleryInfo数据.
        #     if src_file.path not in exit_gly_info_list:
        #         g_info = GalleryInfo()
        #         g_info.folder_key = exist_pic_dirs[src_file.path]
        #         g_info.abs_path = exist_pic_dirs[src_file.path].abs_path
        #         g_info.desc_path = ypath.join(self.desc_middle_root, dir_md5[src_file.path])
        #         g_info.desc_real_path = dir_md5[src_file.path]
        #         g_info.save()
        #         exit_gly_info_list[src_file.path] = g_info
        # # 后组织文件
        # for src_file in src_file_list:
        #     if src_file.is_dir:
        #         continue
        #     if not yutils.is_gif(src_file.ext) and not yutils.is_photo(src_file.ext):
        #         if not self.convert_webp(src_file):
        #             logger.info('PicService.del_not_exist:这文件既不是图片,又不是webp:' + src_file.path)
        #         continue
        #     out_file_name = self.out_file(src_file.relative)
        #     plc = PicHelper.PicLinkCls(exit_gly_info_list[src_file.parent], src_file, dir_md5[src_file.parent],
        #                                out_file_name,
        #                                self.desc_middle_root)
        #     self.file_link_list.append(plc)
        # # 删除文件数据库中没有的数据.
        # # delete_pic_info_db()
        # self.file_link_list.sort(key=lambda x: x.src_file_md5)
        # logger.info('[create_link_dict] end')
        # pass
