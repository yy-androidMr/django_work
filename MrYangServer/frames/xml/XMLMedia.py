# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os
import pathlib

from frames import ypath
from frames.xml import XMLBase


def get_infos():
    dpins = XMLBase.get_base_cfg()
    ss = XMLBase.PROJ_ROOT / '/aa'
    path = XMLBase.PROJ_ROOT / dpins.ins().config_root.innerText / dpins.ins().list.media_info.innerText  # ypath.join(XMLBase.PROJ_ROOT, dpins.ins().config_root.innerText, dpins.ins().list.media_info.innerText)
    if path.exists():
        domPxy = XMLBase.parse(path)
        return domPxy.ins()
