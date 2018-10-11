# -*-coding:utf-8 -*-
from xml.dom import minidom
import os

# 总配置路径
current_path = os.path.dirname(__file__)
CONFIG_INFO_XML = '%s/../../config/configs_info.xml' % current_path
PT_TAG = 'project_root'
CONFIG_TAG = 'config_root'
LIST_TAG = 'list'
# print('current_path:%s,%s' % (current_path, os.getcwd()))


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
        # arg_list[0] = arg_list[0] if arg_list[0] else DomPxy(CONFIG_INFO_XML)
        # return fn(arg_list[0])

    return ins


# 需要尝试使用dom解析,因为Elementtree解析会清除掉注释
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

    # 获取节点的属性
    def attr_value(self, node, attr_name):
        return node.getAttribute(attr_name) if node else ''

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


import os


class DomPxy:
    def __init__(self, path):
        self.path = path
        # print(os.path.abspath('./'))
        self.dom = minidom.parse(path)
        self.elem = ElemPxy(self.dom)

    # def find(self):

    def save(self):
        with open(self.path, 'w', encoding='UTF-8') as fh:
            self.dom.writexml(fh, indent='', encoding='UTF-8')
            # fh.write(self.dom.toprettyxml(encoding='UTF-8'))


# def ins_cfgs_info(dpins=None):
#     dpins = dpins if dpins else DomPxy(CONFIG_INFO_XML)
#     return dpins


# 获取工程路径
@dom_pxy_ins()
def get_pt(dpins=None):
    # 如果没有,则实例化
    proj_root = dpins.elem.value_by_tag(PT_TAG)
    return proj_root, dpins


# 解析configs_info 所有的配置列表
@dom_pxy_ins()
def get_cfg_dir(dpins=None):
    (proj_root, _) = get_pt(dpins)
    config_root = proj_root + dpins.elem.value_by_tag(CONFIG_TAG)
    return config_root.replace('\\', '/'), dpins


# 获取list节点中的某一个配置路径
@dom_pxy_ins()
def cfg_list_path(c_name, dpins=None):
    (config_root, _) = get_cfg_dir(dpins)
    c_p = config_root + dpins.elem.value_by_tag(c_name)
    return c_p.replace('\\', '/'), dpins


def add_attr(node, k, v='', update=False):
    attvalue = node.getAttribute(k)
    if update or not attvalue:
        node.setAttribute(k, v)


def parse(path):
    return DomPxy(path)

#
# path, _ = cfg_list_path('gallery_info')
# dp = DomPxy(path)
# nodelist = dp.elem.xml_nodes('gallery')
# print(dp.elem.attr_value(nodelist[0], 'dir_name'))

# print(c_path('gallery_info'))
