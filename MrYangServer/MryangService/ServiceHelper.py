import datetime
import time

import memory_profiler

from Mryang_App.models import Dir
from frames import ypath, logger
from frames.ypath import PathClass


class TimeWatch:

    def __init__(self, pre):
        self._pre = pre
        self._nowTime = lambda: int(round(time.time() * 1000))
        self._last_tag_time = self._nowTime()
        self.cur_mem = memory_profiler.memory_usage()[0]

    def print_now_time(self, intro):
        logger.info(self._pre + intro + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  占用内存:' + str(
            self.cur_mem) + 'Mb')

    def tag_now(self, intro='', print_it=True, tag_time=True, tag_mem=True):
        now_t = self._nowTime()
        now_mem = memory_profiler.memory_usage()[0]
        if print_it:
            logger.info(
                self._pre + intro + str(now_t - self._last_tag_time) + '毫秒,占用内存:' + str(now_mem) + 'Mb,比较之前上升了:' + str(
                    now_mem - self.cur_mem) + 'Mb')
        self._last_tag_time = now_t
        self.cur_mem = now_mem


def create_dir_root(path, type, tags=''):
    pc = PathClass(path, path)
    try:
        d_model = Dir.objects.get(abs_path=pc.path)
    except Exception as e:
        d_model = Dir()
        d_model.name = pc.name
        d_model.isdir = True
        d_model.abs_path = ypath.convert_path(pc.path)
        d_model.rel_path = pc.relative
        d_model.type = type
        d_model.tags = tags  # if info[ypath.KEYS.LEVEL] == 0 else ''
        d_model.save()
    return d_model


def create_dir(cur_dir_dbs, info, type, tags='', save_it=True):
    name = info.name
    parent_path = info.parent  # info[ypath.KEYS.PARENT]
    rel_path = info.relative
    d_model = Dir()
    d_model.name = name
    d_model.isdir = True
    d_model.abs_path = ypath.convert_path(info.path)
    d_model.rel_path = rel_path
    d_model.type = type
    d_model.tags = tags  # if info[ypath.KEYS.LEVEL] == 0 else ''
    try:
        parent = cur_dir_dbs[parent_path]  # Dir.objects.get(abs_path=parent_path)
        d_model.parent_dir = parent
    except Exception as e:
        logger.info('错误,这货没有爸爸的,忽视这个问题:%s:is not found :%s' % (parent_path, e))
        pass
    if save_it:
        d_model.save()
    return d_model


def compair_db(dbs, desc_path):
    # abs_path
    # desc_path
    file_list = ypath.list_folder(desc_path, include_dir=False)
    db_desc_list = [db.desc_path for db in dbs]
    diff = set(file_list).difference(set(db_desc_list))
    with open('left.txt', 'w+', encoding='utf-8') as f:
        for item in db_desc_list:
            f.write(item + '\n')
    with open('right.txt', 'w+', encoding='utf-8') as f:
        for item in file_list:
            f.write(item + '\n')

    with open('diff.txt', 'w+', encoding='utf-8') as f:
        for item in diff:
            f.write(item + '\n')
    return diff
    # for desc_file in file_list:
    #     if desc_file not in db_desc_list:
    #         print('需要删除的:' + desc_file)


def compair(left_path, right_path):
    left_list = ypath.releative_list(left_path)
    right_list = ypath.releative_list(right_path)
    # db_desc = [desc.desc_path for desc in db_list]
    with open('left.txt', 'w+', encoding='utf-8') as f:
        for item in left_list:
            f.write(item + '\n')
    with open('right.txt', 'w+', encoding='utf-8') as f:
        for item in right_list:
            f.write(item + '\n')
    delete_files = list(set(left_list).difference(set(right_list)))
    # for delete in delete_files:
    #     print(delete)
    return delete_files
