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


def append_ifnot_exist(dir):
    path, _ = XMLBase.c_path(CONFIG_NAME)

    info_root = XMLBase.parseXML(os.path.normpath(path.replace('\\', '/')))
    exist = False
    #查找这个标签原先是不是有.
    for elem in info_root.findall(GALLERY_TAG):
        dir_name = elem.attrib.get(TAGS.DIR_NAME, None)
        if dir_name is not None:
            print(dir_name)
            if dir_name == dir:
                print('找到了:' + dir)
                exist = True
                break


        # print(elem.attrib)
        # gallerys =
        # print(gallerys)


append_ifnot_exist('iuwheruiwirhwioehirhw')
