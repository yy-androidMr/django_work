# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os
from xml.dom import minidom
from frames import ypath
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


class PicBaseInfo:
    def __init__(self):
        self.dir_root = 'dir_root'
        self.thum = 'thum'
        self.middle = 'middle'
        self.item_info = 'item_info'

    def __str__(self):
        return 'dir_root:%s,thum:%s,middle:%s,item_info:%s' % (self.dir_root, self.thum, self.middle, self.item_info)


class PicItemInfo:
    DIR_NAME = 'dir_name'

    def __init__(self):
        self.dir_name = 'dir_name'
        self.name = 'name'
        self.link = 'link'
        self.intro = 'intro'
        self.time = 'time'
        self.thum = 'thum'
        self.level = 'level'
        self.p1 = 'param1'
        self.p2 = 'param2'
        self.value = 'value'


def attr_complition(g_item, dir_name='', link=''):
    info_key = PicItemInfo()
    XMLBase.add_attr(g_item, info_key.dir_name, dir_name)
    XMLBase.add_attr(g_item, info_key.name)
    XMLBase.add_attr(g_item, info_key.link, link)
    XMLBase.add_attr(g_item, info_key.time)
    XMLBase.add_attr(g_item, info_key.thum)
    XMLBase.add_attr(g_item, info_key.level, '0')
    XMLBase.add_attr(g_item, info_key.p1)
    XMLBase.add_attr(g_item, info_key.p2)


def create_gallery_xml(path):
    doc = minidom.Document()
    doc.appendChild(doc.createComment(COMMENT))
    booklist = doc.createElement(CONFIG_NAME)
    doc.appendChild(booklist)
    booklist.appendChild(doc.createTextNode('\n'))
    ypath.create_dirs(path)
    with open(path, 'w', encoding='UTF-8') as fh:
        doc.writexml(fh, indent='', encoding='UTF-8')


def append_ifnot_exist(link_dic):
    if link_dic is None:
        logger.info('append_ifnot_exist:加入配置失败! link_dic')
        return
    domPxy = item_nodes()
    # 查找这个标签原先是不是有.
    for dir in link_dic:
        digout_item = domPxy.elem.has_attr_value(GALLERY_TAG, PicItemInfo.DIR_NAME, dir)
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
    item_info_path = get_infos().item_info  # XMLBase.cfg_list_path(CONFIG_NAME)
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
        iteminfo = PicItemInfo()
        iteminfo.dir_name = domPxy.elem.attr_value(node, iteminfo.dir_name)
        iteminfo.name = domPxy.elem.attr_value(node, iteminfo.name)
        iteminfo.value = domPxy.elem.node_value(node)
        iteminfo.time = domPxy.elem.attr_value(node, iteminfo.time)

        iteminfo.thum = domPxy.elem.attr_value(node, iteminfo.thum)
        iteminfo.level = domPxy.elem.attr_value(node, iteminfo.level)
        iteminfo.p1 = domPxy.elem.attr_value(node, iteminfo.p1)
        iteminfo.p2 = domPxy.elem.attr_value(node, iteminfo.p2)

        xml_infos[iteminfo.dir_name] = iteminfo

    return xml_infos


def get_infos():
    elem_proxy, dpins = nodes()
    pbinfo = PicBaseInfo()
    pbinfo.dir_root = dpins.elem.attr_value(elem_proxy.root, pbinfo.dir_root)
    pbinfo.thum = dpins.elem.attr_value(elem_proxy.root, pbinfo.thum)
    pbinfo.middle = dpins.elem.attr_value(elem_proxy.root, pbinfo.middle)
    pbinfo.item_info = dpins.elem.attr_value(elem_proxy.root, pbinfo.item_info)
    return pbinfo


