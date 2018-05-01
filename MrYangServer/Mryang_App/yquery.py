# -*-coding:utf-8 -*-
import json

from django.db.models import F

from Mryang_App import yutils
from Mryang_App.bats.addPic import PhotoConvert
from Mryang_App.models import Dir


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path')
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def pic_level1_2json():
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, c_id__lt=PhotoConvert.THUM_PIC_ID_POW).values('id', 'tags','name',
                                                                                                     'c_id')
    # show_list = []
    # for d in dirs:
    #     d['tags'] = d['name'].split()
    # item = {'id': d.id, 'p_id': d.p_id, 'isdir': d.isdir, 'tags': d.name.split(), 'path': d.path, 'c_id': d.c_id}
    # show_list.append(item)
    for item in dirs:
        item['tags'] = item['name'].split()
        item.pop('name')

    jsonstr = json.dumps(list(dirs))
    return jsonstr
