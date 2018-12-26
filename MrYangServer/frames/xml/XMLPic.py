# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os
from xml.dom import minidom
from frames import yutils
from frames.logger import logger

from frames.xml import XMLBase


CONFIG_NAME = 'pic_info'
GALLERY_TAG = 'gallery'
COMMENT = '\n<gallery dir_name="a" link="b" name="" param1="" param2="" thum="" time=""> </gallery>' \
          '\n\t\tdir_name:加密后的文件夹名' \
          '\n\t\tlink:加密前的文件夹相对路径' \
          '\n\t\tname:相册展示的标题' \
          '\n\t\t内容txt:副标题' \
          '\n\t\ttime:时间' \
          '\n\t\tthum:指定缩略图' \
          '\n\t\tlevel:展示等级' \
          '\n\t\tparam1,param2:预留接口\n'


class TAGS:
    DIR_ROOT = 'dir_root'
    THUM = 'thum'
    MIDDLE = 'middle'
    ITEM_INFO = 'item_info'
    GIF_BANNER = 'gif_banner'


class ITEM_TAGS:
    DIR_NAME = 'dir_name'
    NAME = 'name'
    LINK = 'link'
    INTRO = 'intro'
    TIME = 'time'
    THUM = 'thum'
    LEVEL = 'level'
    P1 = 'param1'
    P2 = 'param2'
    VALUE = 'value'


def attr_complition(g_item, dir_name='', link=''):
    XMLBase.add_attr(g_item, ITEM_TAGS.DIR_NAME, dir_name)
    XMLBase.add_attr(g_item, ITEM_TAGS.NAME)
    XMLBase.add_attr(g_item, ITEM_TAGS.LINK, link)
    XMLBase.add_attr(g_item, ITEM_TAGS.TIME)
    XMLBase.add_attr(g_item, ITEM_TAGS.THUM)
    XMLBase.add_attr(g_item, ITEM_TAGS.LEVEL, '0')
    XMLBase.add_attr(g_item, ITEM_TAGS.P1)
    XMLBase.add_attr(g_item, ITEM_TAGS.P2)


def create_gallery_xml(path):
    doc = minidom.Document()
    doc.appendChild(doc.createComment(COMMENT))
    booklist = doc.createElement(CONFIG_NAME)
    doc.appendChild(booklist)
    booklist.appendChild(doc.createTextNode('\n'))
    yutils.create_dirs(path)
    with open(path, 'w', encoding='UTF-8') as fh:
        doc.writexml(fh, indent='', encoding='UTF-8')


def append_ifnot_exist(link_dic):
    if link_dic is None:
        logger.info('append_ifnot_exist:加入配置失败! link_dic')
        return
    domPxy = item_nodes()
    # 查找这个标签原先是不是有.
    for dir in link_dic:
        digout_item = domPxy.elem.has_attr_value(GALLERY_TAG, ITEM_TAGS.DIR_NAME, dir)
        if not digout_item:
            digout_item = domPxy.dom.createElement(GALLERY_TAG)
            domPxy.elem.append_child(digout_item)
            digout_item.appendChild(domPxy.dom.createTextNode(' '))

        attr_complition(digout_item, dir, link_dic[dir])
    domPxy.save()


def nodes():
    path, dpins = XMLBase.cfg_list_path(CONFIG_NAME)
    if os.path.exists(path):
        domPxy = XMLBase.parse(path)
        return domPxy.elem, dpins
    return None, dpins


def item_nodes():
    item_info_path = get_infos()[TAGS.ITEM_INFO]  # XMLBase.cfg_list_path(CONFIG_NAME)
    path, _ = XMLBase.get_cfg_dir()
    item_info_path = path + item_info_path
    # 这里需要判断文件是否存在
    if not os.path.exists(item_info_path):
        create_gallery_xml(item_info_path)
    domPxy = XMLBase.parse(item_info_path)
    return domPxy


def get_item_infos():
    domPxy = item_nodes()
    node_list = domPxy.elem.xml_nodes(GALLERY_TAG)
    xml_infos = {}
    for node in node_list:
        dir_name = domPxy.elem.attr_value(node, ITEM_TAGS.DIR_NAME)
        info = {}
        info[ITEM_TAGS.NAME] = domPxy.elem.attr_value(node, ITEM_TAGS.NAME)
        info[ITEM_TAGS.VALUE] = domPxy.elem.node_value(node)
        info[ITEM_TAGS.TIME] = domPxy.elem.attr_value(node, ITEM_TAGS.TIME)

        info[ITEM_TAGS.THUM] = domPxy.elem.attr_value(node, ITEM_TAGS.THUM)
        info[ITEM_TAGS.LEVEL] = domPxy.elem.attr_value(node, ITEM_TAGS.LEVEL)
        info[ITEM_TAGS.P1] = domPxy.elem.attr_value(node, ITEM_TAGS.P1)
        info[ITEM_TAGS.P2] = domPxy.elem.attr_value(node, ITEM_TAGS.P2)

        xml_infos[dir_name] = info

    return xml_infos


def get_infos():
    elem_proxy, dpins = nodes()
    info = {}
    info[TAGS.DIR_ROOT] = dpins.elem.attr_value(elem_proxy.root, TAGS.DIR_ROOT)
    info[TAGS.THUM] = dpins.elem.attr_value(elem_proxy.root, TAGS.THUM)
    info[TAGS.MIDDLE] = dpins.elem.attr_value(elem_proxy.root, TAGS.MIDDLE)
    info[TAGS.ITEM_INFO] = dpins.elem.attr_value(elem_proxy.root, TAGS.ITEM_INFO)

    info[TAGS.GIF_BANNER] = elem_proxy.node_value(elem_proxy.xml_nodes(TAGS.GIF_BANNER)[0])

    return info


print(get_infos())
