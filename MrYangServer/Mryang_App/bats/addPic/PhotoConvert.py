import random

import os

from Mryang_App.bats.ConvertBase import ConvertBase
from Mryang_App import yutils
from Mryang_App.models import Dir

# src->middle->thum
THUM_PIC_ID_POW = 100
LEVEL_TAG_SPLITE = '%'


class PhotoConvert(ConvertBase):
    def __init__(self):
        super().__init__()
        self.dir_id = 1

    def go(self):
        thum_root = '../../../static/media/pic'
        self.insert_dirs(yutils.M_FTYPE_PIC, thum_root, 'thum')

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        if not is_dir:
            if not any(str_ in name for str_ in ('.jpeg', '.jpg')):
                return
        d_model = Dir()
        d_model.name = name
        # d_model.tags = name.split()
        d_model.isdir = is_dir
        d_model.abs_path = abs_path  # 如果数据过大可以考虑不要
        d_model.rel_path = rel_path
        d_model.type = yutils.M_FTYPE_PIC
        d_model.c_id = (self.dir_id if is_dir else 0)
        if is_dir:
            d_model.c_id = self.dir_id
            self.dir_id += 1
        else:
            d_model.parent_dir = parent_dir  # 外键共生
            d_model.c_id = parent_dir.c_id * THUM_PIC_ID_POW  # 照片id为文件夹*100??存疑

        d_model.save()

    def walk_over(self):
        # 结束时,将没有child的dir给删除!!!
        level1 = Dir.objects.filter(c_id__lt=100)
        for l1 in level1:
            childs = Dir.objects.filter(c_id=l1.c_id * THUM_PIC_ID_POW)
            child_count = childs.count()
            if child_count < 1:
                # 删除一级文件夹
                l1.delete()
            else:
                # 这里要读取描述文件
                info_path = l1.abs_path + '/info'
                tags = ''
                info_tags_count = 3
                cur_info_tags = 0
                if os.path.exists(info_path):
                    with open(info_path, encoding='utf-8') as file_object:
                        lines = file_object.readlines()  # 读取全部内容
                        for line in lines:
                            tags += line.rstrip('\n') + ' '
                            cur_info_tags += 1
                if cur_info_tags < info_tags_count:
                    tags += ' ' * (info_tags_count - cur_info_tags)

                tags += childs[random.randrange(0, child_count)].name
                l1.tags = tags
                l1.save()


if __name__ == '__main__':
    # with open(r'G:\pyWorkspace\django_work\MrYangServer\static\media\pic\thum\info', encoding='utf-8') as file_object:
    #     lines = file_object.readlines()  # 读取全部内容
    #     for line in lines:
    #         print(line.rstrip('\n'))
    # PhotoConvert().go()
    PhotoConvert().walk_over()
    # print(Dir.objects.filter(c_id__lt=100))
