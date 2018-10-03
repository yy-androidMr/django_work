# -*-coding:utf-8 -*-
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Avg

from MediaTools.DBTools.addPic import PhotoConvert
from frames import yutils
from Mryang_App.models import *


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    # .extra(select=)
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path', 'name')
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level1_2json(show_level):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    # , type = yutils.M_FTYPE_PIC
    # dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, isdir=True,
    #                           show_level__lt=(show_level + 1)).values('c_id', 'rel_path')
    # ids = [dir['c_id'] for dir in dirs]
    # ginfos = GalleryInfo.objects.filter(level__lt=(show_level + 1)).values('folder_key__c_id',
    #                                                                        'folder_key__rel_path',
    #                                                                        'name',
    #                                                                        'intro',
    #                                                                        'time',
    #                                                                        'thum',
    #                                                                        'level',
    #                                                                        'param1',
    #                                                                        'param2')
    # Avg('s')
    # 1.可能用错了annotate
    # 2.优化1对1的效率
    # 3.extra是别名
    ginfos = GalleryInfo.objects.filter(level__lt=(show_level + 1)).select_related('folder_key').defer(
        'folder_key__id',
        'folder_key__name',
        'folder_key__parent_dir',
        'folder_key__isdir',
        'folder_key__tags',
        'folder_key__abs_path',
        'folder_key__type')
    # GalleryInfo.objects.filter(level__lt=(show_level + 1)).aggregate(folder_key__c_id=F('c_id'))
    return_info = []

    for item in ginfos:
        dict = yutils.to_dict_clear_none(item)
        del dict['isdir']
        print(dict)
        return_info.append(dict)
    # print(yutils.to_dict(ginfos[0]))
    # ginfo_id_dict = {}
    # for ginfo in ginfos:
    #     ginfo_id_dict[ginfo['id']] = ginfo
    #     del ginfo['id']
    #     yutils.dict_clear_none(ginfo)
    #
    # return_info = []
    # for dir in dirs:
    #     return_info.append(dir)
    #     infos = ginfo_id_dict[dir['c_id']]
    #     if infos:
    #         dir.update(infos)
    #
    # jsonstr = json.dumps(return_info)
    # print(jsonstr)
    # return jsonstr
    return return_info


def dead_2json():
    # NOT_SEE
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, c_id__lt=PhotoConvert.THUM_PIC_ID_POW,
                              show_level=99).values('tags',
                                                    'c_id', 'rel_path')
    for item in dirs:
        item['tags'] = item['tags'].split(' ')  # (item['name'] + ' ' + thum).split()
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level2_2json(c_id, page):
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, c_id__lt=(c_id + 1) * PhotoConvert.THUM_PIC_ID_POW,
                              c_id__gt=c_id * PhotoConvert.THUM_PIC_ID_POW).values(
        'tags', 'name', 'c_id').order_by(
        'c_id')
    paginator = Paginator(dirs, 12)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        return ''
        # contacts = paginator.page(1)
    except EmptyPage:
        return ''
        # contacts = paginator.page(1)
    jsonstr = json.dumps(list(contacts.object_list))
    return jsonstr


def upp_json():
    dirs = UpLoadDir.objects.all()
    jsonstr = json.dumps(list(dirs))
    return jsonstr
