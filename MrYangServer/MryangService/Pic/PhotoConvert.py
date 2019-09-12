from MryangService.ServiceHelper import TimeWatch
from MryangService.mpath import MPath
from frames import ypath, logger
from frames.xml import XMLBase

convertIns = None


def start():
    global convertIns
    if convertIns is None:
        convertIns = PConvert()
    convertIns.start()


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

    def src_list(self):
        src_paths = []
        for src_dir in MPath.src_list:
            src_paths.append(ypath.join(src_dir.path, self.src_root))
        return src_paths

    def start(self):
        self.src_dirs = self.src_list()
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

    # 生成middle->(0为不带后缀的相对路径.2为后缀. 1为src) 路径映射
    # @memory_profiler.profile
    def create_link_dict(self):
        for dir in self.src_dirs:
            ypath.del_none_dir(dir)
        pass
