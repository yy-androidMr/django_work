# from MryangService import ServiceHelper
import os
import threading
import time

from django.db import transaction

from MryangService.pic import PicHelper
from MryangService.ServiceHelper import TimeWatch
from Mryang_App import DBHelper
from Mryang_App.models import GalleryInfo, PicInfo
from frames import ypath, logger, TmpUtil, ThreadingPool
from frames.xml import XMLBase

convertIns = None
next_loop_sync = False


def start():
    global next_loop_sync
    next_loop_sync = True
    while True:
        if next_loop_sync:
            global convertIns
            if convertIns is None:
                convertIns = PConvert()
            convertIns.reload()
            next_loop_sync = False
        time.sleep(60)


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
        PicHelper.create_dirs(self.src_dirs, self.src_root, self.webp_cache_root)
        logger.info('[create_dirs] end')
        # # 删除src中没有.middle中有的图.
        # logger.info('PicService.del_not_exist begin!')
        # self.del_not_exist()
        # logger.info('PicService.del_not_exist end!')
        self.watch.tag_now('同步create_dirs时长:')
        db_glys = self.create_gly_info()
        #
        # # 正式转换.
        logger.info('PhotoConvert.begin_convert begin!')
        self.begin_convert(db_glys)
        logger.info('PhotoConvert.begin_convert end!')
        self.watch.tag_now('转换时长:')
        # logger.info('PicService.一个loop走完了.不知道有没有同步完 false 代表同步完了')
        self.handle_db()

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
                else:
                    desc_middle_path = ypath.join(p_info.desc_mpath.dir.abs_path, self.desc_middle_root,
                                                  p_info.gallery_key.desc_real_path,
                                                  p_info.desc_name + p_info.ext)
                    if not os.path.exists(desc_middle_path):
                        p_info.delete()
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
                    mpath = mpath_cache.get(folder.pic_root)
                    if folder.folder_md5 in gly_cache and mpath:
                        # 更新mpath
                        gly_cache[folder.folder_md5].mulit_path.add(mpath)
                    else:
                        g_info = GalleryInfo()
                        g_info.src_real_path = folder.relative
                        g_info.desc_real_path = folder.folder_md5
                        g_info.save()
                        gly_cache[folder.folder_md5] = g_info
                        if mpath:
                            g_info.mulit_path.add(mpath)

        gly_cache = PicHelper.gallery_dict(False)
        mpath_cache = PicHelper.mpath_dict(DBHelper.MPathHelp.SRC, byid=False)

        for src_dir in self.src_dirs:
            ypath.ergodic_folder(src_dir, folder_call_back=folder_call)
        return gly_cache.values()

    def begin_convert(self, db_glys):
        glys_dict = {}
        for db_gly in db_glys:
            glys_dict[db_gly.src_real_path] = db_gly
        all_file_list = PicHelper.get_handle_path_clz(self.src_dirs, self.desc_middle_root, glys_dict)
        fragment_list = {}
        for index, file in enumerate(all_file_list):
            n_ind = index % self.MULIT_THREAD_COUNT
            if n_ind not in fragment_list:
                fragment_list[n_ind] = []
            fragment_list[n_ind].append(file)  # file_link_list[file]
        file_len = len(all_file_list)
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
        create_db_list = []
        err_pic_list = []
        all_mpath_dict = PicHelper.mpath_dict(byid=False)

        for k in fragment_list:
            mtp = MulitThreadParam()
            mtp.f_list = fragment_list[k]
            mtp.create_db_list = create_db_list
            mtp.err_list = err_pic_list
            mtp.db_glys = glys_dict
            mtp.desc_middle_root = self.desc_middle_root
            mtp.desc_thum_root = self.desc_thum_root
            mtp.middle_area = self.middle_area
            mtp.thum_size = self.thum_size
            mtp.all_mpath_dict = all_mpath_dict
            tpool.append(PicHelper.begin_threads, mtp)
        tpool.start()
        self.watch.tag_now('图片同步结束:')
        if len(create_db_list) > 0:
            PicInfo.objects.bulk_create(create_db_list)

    # 处理数据库里面不相符的图.
    def handle_db(self):
        with open(os.path.join(TmpUtil.tmpdir, 'err.txt'), 'w+', encoding='utf-8') as f:
            for item in self.err_pic:
                f.write(item + '\n')
        pass


# 重新同步.
def sync_on_back():
    global next_loop_sync
    if next_loop_sync:
        return {'res': 3, 'res_str': '正在同步中请稍等...'}
    next_loop_sync = True
    return {'res': 1, 'res_str': '同步请求发送成功!'}
    # return {'res': 2, 'res_str': '同步请求失败!正在同步中...'}


# 多线程的参数
class MulitThreadParam:
    pass
