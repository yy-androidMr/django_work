# -*-coding:utf-8 -*-
import xml.dom.minidom
import xml.sax

# 总配置路径
CONFIG_INFO_XML = "../config/configs_info.xml"


class ConfigsHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.PROJECT_ROOT_STR = 'project_root'
        self.CONFIG_ROOT_STR = 'config_root'
        self.LIST_STR = 'list'
        self.curElement = ''
        self.project_root = ''
        self.config_root = ''
        self.config_paths = []

    def startElement(self, name, attrs):
        self.curElement = name
        # print('startElemetn:' + name, '   attrs:' + str(attrs))
        pass

    def endElement(self, name):
        print('endElement:' + name)
        pass

    def characters(self, content):
        print('characters:' + content)
        pass


def get_configs_root():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespace_prefixes, 0)
    handler = ConfigsHandler()
    parser.setContentHandler(handler)
    parser.parse(CONFIG_INFO_XML)
    # dom = xml.dom.minidom.parse(CONFIG_INFO_XML)
    # root = dom.documentElement
    # return root


get_configs_root()
