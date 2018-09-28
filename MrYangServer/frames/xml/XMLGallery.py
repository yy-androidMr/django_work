# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
from frames.xml import XMLBase

CONFIG_NAME = 'gallery_info'


def append_ifnot_exist():
    path = XMLBase.c_path(CONFIG_NAME)

    info_root = XMLBase.parseXML(path)
    for elem in info_root.findall('gallery'):
        pass
    # gallerys =
    print(gallerys)
