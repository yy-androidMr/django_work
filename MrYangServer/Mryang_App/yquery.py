# -*-coding:utf-8 -*-
import json

from django.db.models import F

from MediaTools.DBTools.addPic import PhotoConvert
from frames import yutils
from Mryang_App.models import *


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path', 'name')
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level1_2json(show_level):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    ginfos = GalleryInfo.objects.filter(level__lt=(show_level + 1)).annotate(
        c_id=F('folder_key__c_id'), rel_path=F('folder_key__rel_path')) \
        .select_related('folder_key') \
        .values('name', 'intro', 'time', 'thum', 'level', 'param1', 'param2', 'c_id', 'rel_path')
    return_list = list(ginfos)
    yutils.list_clear_none(return_list)
    print('一次查询----------')

    json_res = json.dumps(return_list)
    print('查询结果:%s' % json_res)
    return json_res


def dead_2json():
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, c_id__lt=PhotoConvert.THUM_PIC_ID_POW,
                              show_level=99).values('tags',
                                                    'c_id', 'rel_path')
    for item in dirs:
        item['tags'] = item['tags'].split(' ')  # (item['name'] + ' ' + thum).split()
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level2_2json(c_id, page):
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, isdir=False, parent_dir__c_id=c_id) \
        .select_related('parent_dir').values('tags', 'name', 'c_id').order_by('c_id')

    page_item = 12
    page -= 1
    bottom = page * page_item
    top = bottom + page_item
    # if top > dirs.count():
    #     top = dirs.count()
    list_data = list(dirs[bottom:top])
    print(list_data)

    # paginator = Paginator(dirs, 12)
    # try:
    #     contacts = paginator.page(page)
    # except PageNotAnInteger:
    #     print('[pic_level2_2json]:', PageNotAnInteger)
    #     return ''
    # except EmptyPage:
    #     print('[pic_level2_2json]:', EmptyPage)
    #     return ''
    jsonstr = json.dumps(list_data)
    # jsonstr = ''
    return jsonstr


def upp_json():
    dirs = UpLoadDir.objects.all()
    jsonstr = json.dumps(list(dirs))
    return jsonstr
