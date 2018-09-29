# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os

from frames.xml import XMLBase

CONFIG_NAME = 'gallery_info'
GALLERY_TAG = 'gallery'


class TAGS:
    DIR_NAME = 'dir_name'
    NAME = 'name'
    TIME = 'time'
    THUM = 'thum'
    P1 = 'param1'
    P2 = 'param2'


def attr_complition(g_item, dir_name=''):
    XMLBase.add_attr(g_item, TAGS.DIR_NAME, dir_name)
    XMLBase.add_attr(g_item, TAGS.NAME)
    XMLBase.add_attr(g_item, TAGS.TIME)
    XMLBase.add_attr(g_item, TAGS.THUM)
    XMLBase.add_attr(g_item, TAGS.P1)
    XMLBase.add_attr(g_item, TAGS.P2)


def append_ifnot_exist(dir):
    path, _ = XMLBase.c_path(CONFIG_NAME)

    tree, info_root = XMLBase.parseXML(path)
    # 查找这个标签原先是不是有.
    g_item = None
    for elem in info_root.findall(GALLERY_TAG):
        dir_name = elem.attrib.get(TAGS.DIR_NAME, None)
        if dir_name is not None:
            print(dir_name)
            if dir_name == dir:
                g_item = elem
                print('找到了:' + dir)
                break

    if g_item is not None:
        attr_complition(g_item)
        XMLBase.dump(info_root)
        tree.write(path, encoding="utf-8", xml_declaration=True,short_empty_elements=False)
        # print(elem.attrib)
        # gallerys =
        # print(gallerys)


append_ifnot_exist('iuwheruiwirhwioehirhw')
