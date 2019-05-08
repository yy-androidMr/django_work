# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os

from frames import ypath
from frames.xml import XMLBase


def get_infos():
    dpins = XMLBase.get_base_cfg()
    path = ypath.join(XMLBase.PROJ_ROOT, dpins.ins().config_root.innerText, dpins.ins().list.media_info.innerText)
    if os.path.exists(path):
        domPxy = XMLBase.parse(path)
        return domPxy.ins()
