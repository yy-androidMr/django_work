# -*-coding:utf-8 -*-

from xml.etree import ElementTree as ET

# 总配置路径
CONFIG_INFO_XML = '../../config/configs_info.xml'
PT_TAG = 'project_root'
CONFIG_TAG = 'config_root'
LIST_TAG = 'list'


# 解析xml
def parseXML(path):
    # api
    # class xml.etree.ElementTree.Element(tag, attrib={}, ** extra)
    #
    # 　　tag：string，元素代表的数据种类。
    # 　　text：string，元素的内容。
    # 　　tail：string，元素的尾形。
    # 　　attrib：dictionary，元素的属性字典。
    # 　　
    # 　　＃针对属性的操作
    # 　　clear()：清空元素的后代、属性、text和tail也设置为None。
    # 　　get(key, default=None)：获取key对应的属性值，如该属性不存在则返回default值。
    # 　　items()：根据属性字典返回一个列表，列表元素为(key, value）。
    # 　　keys()：返回包含所有元素属性键的列表。
    # 　　set(key, value)：设置新的属性键与值。
    #
    # 　　＃针对后代的操作
    # 　　append(subelement)：添加直系子元素。
    # 　　extend(subelements)：增加一串元素对象作为子元素。＃python2
    # .7
    # 新特性
    # 　　find(match)：寻找第一个匹配子元素，匹配对象可以为tag或path。
    # 　　findall(match)：寻找所有匹配子元素，匹配对象可以为tag或path。
    # 　　findtext(match)：寻找第一个匹配子元素，返回其text值。匹配对象可以为tag或path。
    # 　　insert(index, element)：在指定位置插入子元素。
    # 　　iter(tag=None)：生成遍历当前元素所有后代或者给定tag的后代的迭代器。＃python2
    # .7
    # 新特性
    # 　　iterfind(match)：根据tag或path查找所有的后代。
    # 　　itertext()：遍历所有后代并返回text值。
    # 　　remove(subelement)：删除子元素。
    #
    root = ET.parse(path).getroot()
    return root


# 解析configs_info 所有的配置列表
def get_configs_root():
    return parseXML(CONFIG_INFO_XML)


# 获取工程路径
def get_pt(d_root=None):
    if d_root is None:
        d_root = get_configs_root()
    pt_text = d_root.find(PT_TAG)
    return pt_text, d_root


# 获取整个配置文件夹路径
def get_confg_dir(d_root=None):
    if d_root is None:
        d_root = get_configs_root()
    (pt_root, _) = get_pt(d_root)
    c_root = pt_root.text + d_root.find(CONFIG_TAG).text
    return c_root, d_root


# 获取list节点中的某一个配置路径
def c_path(c_name, d_root=None):
    if d_root is None:
        d_root = get_configs_root()
    (c_root, _) = get_confg_dir(d_root)
    c_p = c_root + d_root.find(LIST_TAG).find(c_name).text
    return c_p, d_root

# print(c_path('gallery_info'))
