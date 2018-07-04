# -*-coding:utf-8 -*-
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F

from MediaTools.DBTools.addPic import PhotoConvert
from Mryang_App import yutils
from Mryang_App.models import Dir, UpLoadDir


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path', 'name')
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level1_2json(show_level):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, c_id__lt=PhotoConvert.THUM_PIC_ID_POW,
                              show_level__lt=(show_level + 1)).values('tags',
                                                                      'c_id', 'rel_path')
    for item in dirs:
        item['tags'] = item['tags'].split(' ')  # (item['name'] + ' ' + thum).split()
    jsonstr = json.dumps(list(dirs))
    return jsonstr


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
