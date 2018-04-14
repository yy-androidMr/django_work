# -*-coding:utf-8 -*-
import json

from django.db.models import F

from Mryang_App import yutils
from Mryang_App.models import Dir


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path')
    jsonstr = json.dumps(list(dirs))
    return jsonstr
