# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os
from xml.dom import minidom

from frames.xml import XMLBase
from frames import yutils

CONFIG_NAME = 'movie_info'
ITEM_TAG = 'item'
INFO_TAG = 'm3u8_info'


class TAGS:
    DIR_ROOT = 'dir_root'
    DIR_EXTEN = 'dir_exten'
    INFO_FILE = 'info_file'
    NAME = 'name'
    CONVERT_DIR = 'convert_dir'
    OUT_DIR = 'out_dir'
    TS_DIR = 'ts_dir'
    ITEM_INFO = 'item_info'
    VALUE = 'value'


class ITEM_TAGS:
    FILE = 'file'
    NAME = 'name'
    SIZE = 'size'
    SHOW_SIZE = 'show_size'
    DURATION = 'duration'
    SHOW_DURATION = 'show_duration'
    OUT_NAME = 'out_name'  # 输出的ym3的文件名
    PIXEL = 'source_size'
    FPS = 'fps'


def nodes():
    path, dpins = XMLBase.cfg_list_path(CONFIG_NAME)
    if os.path.exists(path):
        domPxy = XMLBase.parse(path)
        return domPxy.elem, dpins
    return None, dpins


def get_infos():
    elem_proxy, dpins = nodes()
    node = elem_proxy.xml_nodes(INFO_TAG)[0]
    info = {}
    info[TAGS.DIR_ROOT] = dpins.elem.attr_value(elem_proxy.root, TAGS.DIR_ROOT)
    info[TAGS.DIR_EXTEN] = dpins.elem.attr_value(node, TAGS.DIR_EXTEN)
    info[TAGS.INFO_FILE] = dpins.elem.attr_value(node, TAGS.INFO_FILE)
    info[TAGS.NAME] = dpins.elem.attr_value(node, TAGS.NAME)
    info[TAGS.CONVERT_DIR] = dpins.elem.attr_value(node, TAGS.CONVERT_DIR)
    info[TAGS.OUT_DIR] = dpins.elem.attr_value(node, TAGS.OUT_DIR)
    info[TAGS.TS_DIR] = dpins.elem.attr_value(node, TAGS.TS_DIR)
    info[TAGS.ITEM_INFO] = dpins.elem.attr_value(node, TAGS.ITEM_INFO)

    return info


def create_movie_item_info_xml(item_info_list):
    movie_item_info_path = get_infos()[TAGS.ITEM_INFO]
    doc = minidom.Document()
    booklist = doc.createElement(CONFIG_NAME)
    doc.appendChild(booklist)
    booklist.appendChild(doc.createTextNode('\n'))
    path, _ = XMLBase.get_cfg_dir()
    movie_item_info_path = path + movie_item_info_path
    yutils.create_dirs(movie_item_info_path)

    for item_info in item_info_list:
        item = doc.createElement(ITEM_TAG)
        booklist.appendChild(item)
        item.setAttribute(ITEM_TAGS.FILE, item_info[ITEM_TAGS.FILE])
        item.setAttribute(ITEM_TAGS.NAME, item_info[ITEM_TAGS.NAME])
        item.setAttribute(ITEM_TAGS.SIZE, item_info[ITEM_TAGS.SIZE])
        item.setAttribute(ITEM_TAGS.SHOW_SIZE, item_info[ITEM_TAGS.SHOW_SIZE])
        item.setAttribute(ITEM_TAGS.DURATION, item_info[ITEM_TAGS.DURATION])
        item.setAttribute(ITEM_TAGS.SHOW_DURATION, item_info[ITEM_TAGS.SHOW_DURATION])
        item.setAttribute(ITEM_TAGS.OUT_NAME, item_info[ITEM_TAGS.OUT_NAME])
        item.setAttribute(ITEM_TAGS.PIXEL, item_info[ITEM_TAGS.PIXEL])
        item.setAttribute(ITEM_TAGS.FPS, item_info[ITEM_TAGS.FPS])

    with open(movie_item_info_path, 'w', encoding='UTF-8') as fh:
        doc.writexml(fh, indent='', encoding='UTF-8', newl='\n')


def item_info_dict():
    # key name value []
    infos = {}
    path, _ = XMLBase.get_cfg_dir()
    movie_item_info_path = get_infos()[TAGS.ITEM_INFO]
    movie_item_info_path = path + movie_item_info_path

    nodes = XMLBase.parse(movie_item_info_path).elem.xml_nodes(ITEM_TAG)
    for node in nodes:
        items = {}
        infos[node.getAttribute(ITEM_TAGS.OUT_NAME)] = items
        items[ITEM_TAGS.FILE] = node.getAttribute(ITEM_TAGS.FILE)
        items[ITEM_TAGS.NAME] = node.getAttribute(ITEM_TAGS.NAME)
        items[ITEM_TAGS.SIZE] = node.getAttribute(ITEM_TAGS.SIZE)
        items[ITEM_TAGS.SHOW_SIZE] = node.getAttribute(ITEM_TAGS.SHOW_SIZE)
        items[ITEM_TAGS.DURATION] = node.getAttribute(ITEM_TAGS.DURATION)
        items[ITEM_TAGS.SHOW_DURATION] = node.getAttribute(ITEM_TAGS.SHOW_DURATION)
        items[ITEM_TAGS.PIXEL] = node.getAttribute(ITEM_TAGS.PIXEL)
        items[ITEM_TAGS.FPS] = node.getAttribute(ITEM_TAGS.FPS)
    return infos


def movie_url(dpins=None):
    res_url, res_root = XMLBase.res_url_info(dpins)
