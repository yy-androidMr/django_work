import random
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
django.setup()

from frames import yutils, ypath, TmpUtil
from Mryang_Tdb.models import Dir, GalleryInfo

# src->middle->thum
from frames.xml import XMLPic

pic_cfg = XMLPic.get_infos()


def insert_gallery_info():
    GalleryInfo.objects.all().delete()

    # 结束时,将没有child的dir给删除!!!
    level1 = Dir.objects.filter(isdir=True, type=yutils.M_FTYPE_PIC)
    for l1 in level1:
        childs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, isdir=False, parent_dir=l1)  # 查找区间内的id
        child_count = childs.count()
        if child_count < 1:
            # 删除一级文件夹
            l1.delete()
        else:
            new_info_convert(l1, childs[random.randrange(0, child_count)], XMLPic.get_item_infos())
    print('done')


def new_info_convert(l1, child_dir, xml_infos):
    info = xml_infos[l1.name]
    gallery_list = []
    g_info = GalleryInfo()
    gallery_list.append(g_info)
    g_info.folder_key = l1
    g_info.dir_name = l1.name
    g_info.id = l1.c_id
    if info:
        g_info.name = info[XMLPic.ITEM_TAGS.NAME]
        g_info.intro = info[XMLPic.ITEM_TAGS.VALUE]
        g_info.time = info[XMLPic.ITEM_TAGS.TIME]
        g_info.thum = info[XMLPic.ITEM_TAGS.THUM] if info[XMLPic.ITEM_TAGS.THUM] else child_dir.name
        g_info.level = int(info[XMLPic.ITEM_TAGS.LEVEL]) if info[XMLPic.ITEM_TAGS.LEVEL] else 0

        g_info.param1 = info[XMLPic.ITEM_TAGS.P1]
        g_info.param2 = info[XMLPic.ITEM_TAGS.P2]
    else:
        print('无该配置!:' + l1.name)
    GalleryInfo.objects.bulk_create(gallery_list)


def insert_db(dir_list, file_list):
    dir_id = 1
    dir_db_list = {}
    for item in dir_list:
        infos = item[1]
        abs_path = item[0]
        d_model = Dir()
        d_model.name = infos[ypath.KEYS.NAME]
        # d_model.tags = name.split()
        d_model.isdir = infos[ypath.KEYS.IS_DIR]
        d_model.abs_path = abs_path  # 如果数据过大可以考虑不要
        d_model.rel_path = infos[ypath.KEYS.REL]
        d_model.type = yutils.M_FTYPE_PIC
        d_model.c_id = dir_id
        dir_id += 1

        try:
            parent = Dir.objects.get(abs_path=infos[ypath.KEYS.PARENT])
            d_model.parent_dir = parent
        except Exception as e:
            print('错误:%s:is not found :%s' % (infos[ypath.KEYS.PARENT], e))
            pass
        d_model.save()
        dir_db_list[d_model.abs_path] = d_model

    file_dirdb_list = []
    for item in file_list:
        infos = item[1]
        abs_path = item[0]
        d_model = Dir()
        d_model.name = infos[ypath.KEYS.NAME]
        d_model.isdir = infos[ypath.KEYS.IS_DIR]
        d_model.abs_path = abs_path
        d_model.rel_path = infos[ypath.KEYS.REL]
        d_model.type = yutils.M_FTYPE_PIC

        d_model.parent_dir = dir_db_list[infos[ypath.KEYS.PARENT]]
        d_model.c_id = dir_id  # 照片id为文件夹*100??存疑
        dir_id += 1

        file_dirdb_list.append(d_model)
    return file_dirdb_list


def read_thum():
    Dir.objects.filter(type=yutils.M_FTYPE_PIC).delete()
    desc = TmpUtil.get(yutils.RESOURCE_DESC_KEY)
    desc = ypath.join(desc, pic_cfg[XMLPic.TAGS.DIR_ROOT])
    dict = ypath.path_result(desc, pic_cfg[XMLPic.TAGS.THUM], add_root=False)
    dir_dict = {}
    file_dict = {}
    for key in dict:
        if (dict[key][ypath.KEYS.IS_DIR]):
            dir_dict[key] = dict[key]
        else:
            file_dict[key] = dict[key]

    dir_list = sorted(dir_dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])
    file_list = sorted(file_dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])

    file_db_list = insert_db(dir_list, file_list)
    Dir.objects.bulk_create(file_db_list)


if __name__ == '__main__':
    read_thum()
    insert_gallery_info()
