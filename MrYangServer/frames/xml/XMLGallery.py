# -*-coding:utf-8 -*-

#每个解析都有个名字.对应configs_info配置中的configs_info->list
from . import XMLBase

CONFIG_NAME = 'gallery_info'

def append():
    path = XMLBase.c_path(CONFIG_NAME)
    print(path)