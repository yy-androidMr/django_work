# -*-coding:utf-8 -*-
from xml.dom import minidom

# 总配置路径
from xml.dom.minidom import Element, Text

import manage

PROJ_ROOT = manage.root()
CONFIG_INFO_XML = PROJ_ROOT / 'config/configs_info.xml'
GIF_BANNER = 'gif_banner'
COS_MEDIA_ROOT = 'cos_media_root'
RES_URL = 'res_url'
LIST_TAG = 'list'


# 功能:注解参数:dpins=1  代表args的第二个加上dompxy
def dom_pxy_ins(*annokwds):
    def ins(f):
        def new_f(*args, **kwargs):
            tag_cfg_name = None
            for arg in args:
                if type(arg) == DomPxy:
                    tag_cfg_name = arg.path

            for k in kwargs:
                if type(kwargs[k]) == DomPxy:
                    tag_cfg_name = arg.path
            print('fun:%s, has pxy:%s' % (str(f), tag_cfg_name))
            if tag_cfg_name:
                return f(*args, **kwargs)

            if len(annokwds) > 0:
                kwargs[annokwds[0]] = DomPxy(CONFIG_INFO_XML)
            else:
                # 这里对参数第一个添加上DomPxy
                arg_list = list(args)
                arg_list.append(DomPxy(CONFIG_INFO_XML))
                args = tuple(arg_list)
            return f(*args, **kwargs)

        return new_f

    return ins


# 需要尝试使用dom解析,因为Elementtree解析会清除掉注释  #  调整完XMLPic  要删除!!
class ElemPxy:
    def __init__(self, dom):
        self.dom = dom
        self.root = dom.documentElement

    # 获取节点
    def xml_nodes(self, tag):
        return self.root.getElementsByTagName(tag) if self.root else []

    # 获取节点的内容
    def node_value(self, node, index=0):
        return node.childNodes[index].nodeValue if node else ''

    def attr_value(self, node, attr_name):
        return node.getAttribute(attr_name) if node else ''

    # 获取节点的属性

    # 根据节点名,直接获取节点内容
    def value_by_tag(self, tag, node_index=0, index=0):
        nodes = self.xml_nodes(tag)
        # 三目运算
        return self.node_value(nodes[node_index], index) if len(nodes) > 0 else ''
        # if len(nodes) > 0:

    def has_attr_value(self, tag, attr_name, value):
        node_list = self.xml_nodes(tag)
        for item in node_list:
            if self.attr_value(item, attr_name) == value:
                return item
        return None

    def append_child(self, node):
        self.root.appendChild(self.dom.createTextNode('\t'))
        self.root.appendChild(node)
        self.root.appendChild(self.dom.createTextNode('\n'))


class DomPxy:
    def __init__(self, path):
        self.path = path
        # print(os.path.abspath('./'))
        self.dom = minidom.parse(str(path))
        self.elem = ElemPxy(self.dom)
        self.instance = None

    #  调整完XMLPic  要删除!!
    def save(self):

        with self.path.open('w', encoding='UTF-8') as fh:
            self.dom.writexml(fh, indent='', encoding='UTF-8')
            # fh.write(self.dom.toprettyxml(encoding='UTF-8'))

    def ins(self):
        if self.instance:
            return self.instance
        # 获取实例
        self.instance = XmlBean()
        self.insert_child_attr(self.dom.documentElement, self.instance)
        return self.instance

    def insert_child_attr(self, node, parent):
        ats = node.attributes
        if ats._attrs is not None:
            for k in ats._attrs:
                setattr(parent, k, node.getAttribute(k))
        child_dict = {}
        for child in node.childNodes:
            if type(child) == Element:
                if not child_dict.get(child.tagName):
                    child_dict[child.tagName] = []
                child_dict[child.tagName].append(child)

        if len(node.childNodes) == 1 and type(node.childNodes[0]) == Text:
            setattr(parent, "innerText", node.childNodes[0].nodeValue)

        for c_name in child_dict:
            c_nodes = child_dict[c_name]
            if len(c_nodes) == 1:
                c_ins = XmlBean()
                setattr(parent, c_name, c_ins)
                self.insert_child_attr(c_nodes[0], c_ins)
            else:
                ins_list = [XmlBean() for _ in range(len(c_nodes))]
                setattr(parent, c_name, ins_list)
                index = 0
                for item in c_nodes:
                    self.insert_child_attr(item, ins_list[index])
                    index += 1


# 解析configs_info 所有的配置列表
@dom_pxy_ins()
def get_base_cfg(dpins=None):
    return dpins


#  调整完XMLPic  要删除!!
@dom_pxy_ins()
def get_cfg_dir(dpins=None):
    ins = dpins.ins()
    config_root = PROJ_ROOT / ins.config_root.innerText
    return config_root.replace('\\', '/'), dpins


#  调整完XMLPic  要删除!!
def add_attr(node, k, v='', update=False):
    attvalue = node.getAttribute(k)
    if update or not attvalue:
        node.setAttribute(k, v)


def parse(path):
    return DomPxy(path)


# 序列化的实例,每个配置自己用反射添加内容
class XmlBean(object):
    pass
