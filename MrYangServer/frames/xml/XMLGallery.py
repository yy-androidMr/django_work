# -*-coding:utf-8 -*-

# 每个解析都有个名字.对应configs_info配置中的configs_info->list
import os
from xml.dom import minidom

from frames.xml import XMLBase

CONFIG_NAME = 'gallery_info'
GALLERY_TAG = 'gallery'
COMMENT = '\n<gallery dir_name="a" link="b" name="" param1="" param2="" thum="" time=""> </gallery>' \
          '\n\t\tdir_name:加密后的文件夹名' \
          '\n\t\tlink:加密前的文件夹相对路径' \
          '\n\t\tname:相册展示的标题' \
          '\n\t\t内容txt:副标题' \
          '\n\t\ttime:时间' \
          '\n\t\tthum:指定缩略图' \
          '\n\t\tparam1,param2:预留接口\n'


class TAGS:
    DIR_NAME = 'dir_name'
    NAME = 'name'
    LINK = 'link'
    INTRO = 'intro'
    TIME = 'time'
    THUM = 'thum'
    P1 = 'param1'
    P2 = 'param2'


def attr_complition(g_item, dir_name='', link=''):
    XMLBase.add_attr(g_item, TAGS.DIR_NAME, dir_name)
    XMLBase.add_attr(g_item, TAGS.NAME)
    XMLBase.add_attr(g_item, TAGS.LINK, link)
    XMLBase.add_attr(g_item, TAGS.TIME)
    XMLBase.add_attr(g_item, TAGS.THUM)
    XMLBase.add_attr(g_item, TAGS.P1)
    XMLBase.add_attr(g_item, TAGS.P2)


def create_gallery_xml(path):
    doc = minidom.Document()
    doc.appendChild(doc.createComment(COMMENT))
    booklist = doc.createElement(CONFIG_NAME)
    doc.appendChild(booklist)
    booklist.appendChild(doc.createTextNode('\n'))

    with open(path, 'w', encoding='UTF-8') as fh:
        doc.writexml(fh, indent='', encoding='UTF-8')


def append_ifnot_exist(link_dic):
    path, _ = XMLBase.cfg_list_path(CONFIG_NAME)
    # 这里需要判断文件是否存在
    if not os.path.exists(path):
        create_gallery_xml(path)
    domPxy = XMLBase.parse(path)
    # 查找这个标签原先是不是有.
    for dir in link_dic:
        digout_item = domPxy.elem.has_attr_value(GALLERY_TAG, TAGS.DIR_NAME, dir)
        if not digout_item:
            digout_item = domPxy.dom.createElement(GALLERY_TAG)
            domPxy.elem.append_child(digout_item)
            digout_item.appendChild(domPxy.dom.createTextNode(' '))

        attr_complition(digout_item, dir, link_dic[dir])
    domPxy.save()
