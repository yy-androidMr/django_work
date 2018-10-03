import random

from MediaTools.DBTools.ConvertBase import ConvertBase
from frames import yutils
from Mryang_App.models import Dir, GalleryInfo

# src->middle->thum
from frames.xml import XMLGallery

THUM_PIC_ID_POW = 100000
LEVEL_TAG_SPLITE = '%'
LEVEL_INDEX = 4


class PhotoConvert(ConvertBase):
    def __init__(self):
        super().__init__(4)
        self.dir_id = 1
        self.child_id = {}
        self.dir_list = []

    def go(self):
        self.insert_dirs(yutils.M_FTYPE_PIC, self.media_root + '/pic', 'thum')

    def walk_call(self, abs_path, rel_path, parent_dir, name, is_dir):
        if not is_dir:
            if not any(str_ in name.lower() for str_ in ('.jpg', 'jpeg', 'png', 'gif')):
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
            d_model.save()
        else:
            d_model.parent_dir = parent_dir  # 外键共生
            c_id = parent_dir.c_id * THUM_PIC_ID_POW
            cur_child_id = 1
            if parent_dir.c_id in self.child_id:
                cur_child_id = self.child_id[parent_dir.c_id]
                cur_child_id += 1
            self.child_id[parent_dir.c_id] = cur_child_id
            # self.child_id[str(parent_dir.c_id)] = cur_child_id
            c_id += cur_child_id
            print(str(c_id) + " type:" + str(type(parent_dir.c_id * THUM_PIC_ID_POW)) + "  type2:" + str(type(c_id)))
            d_model.c_id = c_id  # 照片id为文件夹*100??存疑
            # d_model.save()
            self.dir_list.append(d_model)
        print(rel_path)

    def walk_over(self):
        # if self.dir_list.count() > 0:
        Dir.objects.bulk_create(self.dir_list)
        GalleryInfo.objects.all().delete()
        xml_infos = XMLGallery.get_infos()

        # 结束时,将没有child的dir给删除!!!
        level1 = Dir.objects.filter(isdir=True, type=yutils.M_FTYPE_PIC)
        for l1 in level1:
            childs = Dir.objects.filter(c_id__lt=(l1.c_id + 1) * THUM_PIC_ID_POW,
                                        c_id__gt=l1.c_id * THUM_PIC_ID_POW)  # 查找区间内的id
            child_count = childs.count()
            if child_count < 1:
                # 删除一级文件夹
                l1.delete()
            else:
                self.new_info_convert(l1, childs[random.randrange(0, child_count)], xml_infos)
        print('done')

    def new_info_convert(self, l1, child_dir, xml_infos):
        info = xml_infos[l1.name]
        g_info = GalleryInfo()
        g_info.folder_key = l1
        g_info.dir_name = l1.name
        g_info.id = l1.c_id
        if info:
            g_info.name = info[0]
            g_info.intro = info[1]
            g_info.time = info[2]
            g_info.thum = info[3] if info[3] else child_dir.name
            g_info.level = int(info[4]) if info[4] else 0

            g_info.param1 = info[5]
            g_info.param2 = info[6]
        else:
            print('无该配置!:' + l1.name)
        g_info.save()


# if __name__ == '__main__':
#     PhotoConvert().go()

# for p in GalleryInfo.objects.raw('SELECT id, name FROM Mryang_App_galleryinfo'):
#     print(p)

# for p in Dir.objects.raw(r'SELECT "Mryang_App_dir"."id", "Mryang_App_dir"."name" FROM "Mryang_App_dir"'):
#     print(p)
# print()
# for p in GalleryInfo.objects.raw(
#         r'SELECT  FROM "Mryang_App_galleryinfo"'):
#     print(p)
#     pass
# print('done')


# print(GalleryInfo.objects.filter(level=0))
