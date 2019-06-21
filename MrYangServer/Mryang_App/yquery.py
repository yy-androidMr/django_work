# -*-coding:utf-8 -*-
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F

from Mryang_App import DBHelper
from frames import yutils
from Mryang_App.models import *
from frames.logger import logger


def dir_2json(dirtype):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    dirs = Dir.objects.annotate(p_id=F('parent_dir__id'), path=F('rel_path')) \
        .filter(type=dirtype).values('id', 'p_id', 'isdir', 'tags', 'path', 'name')
    jsonstr = json.dumps(list(dirs))
    return jsonstr


def meida_root(tags):
    root_dir = Dir.objects.get(tags=tags, parent_dir=None)
    return media_dir(tags, root_dir.id)


def media_dir(tags, p_id):
    dinfos = Dir.objects.annotate(p_id=F('parent_dir__id')).filter(tags=tags, parent_dir_id=p_id).values(
        'id', 'name')
    minfos = Media.objects.filter(folder_key=p_id, state=DBHelper.end_media_state()).values('nginx_path',
                                                                                            'duration',
                                                                                            'size',
                                                                                            'width',
                                                                                            'height',
                                                                                            'r_frame_rate')
    res = {'dir': list(dinfos), 'info': list(minfos)}
    json_res = json.dumps(res)
    return json_res


# def movie_infos():
#     infos = MediaInfo.objects.annotate(d_id=F('folder_key__id')).values('d_id', 'name', 'duration', 'size',
#                                                                        'source_size', 'fps')
#     jsonstr = json.dumps(list(infos))
#     return jsonstr


def pic_level1_2json(show_level):
    # id  名字, 父亲的id, 是否是文件夹, tag, 相对路径.
    from Mryang_App.models import GalleryInfo
    ginfos = GalleryInfo.objects.filter(level__lt=(show_level + 1)).annotate(
        c_id=F('folder_key__id'), rel_path=F('folder_key__rel_path')) \
        .select_related('folder_key') \
        .values('name', 'intro', 'time', 'thum', 'level', 'param1', 'param2', 'c_id', 'rel_path')
    return_list = list(ginfos)
    yutils.list_clear_none(return_list)
    print('一次查询----------')

    json_res = json.dumps(return_list)
    logger.debug('查询结果:', json_res)
    return json_res


def pic_level2_2json(c_id, page):
    from Mryang_App.models import Dir
    # 好像c_id没吊jb用
    dirs = Dir.objects.filter(type=yutils.M_FTYPE_PIC, isdir=False, parent_dir__id=c_id) \
        .select_related('parent_dir').values('tags', 'name', 'c_id').order_by('c_id')

    page_item = 30
    # page -= 1
    # bottom = page * page_item
    # top = bottom + page_item
    # dirs_count = dirs.count()
    # if bottom > dirs_count:
    #     return ''
    # elif top > dirs_count:
    #     top = dirs_count
    # list_data = list(dirs[bottom:top])
    # print(list_data)

    paginator = Paginator(dirs, page_item)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        print('[pic_level2_2json]:', PageNotAnInteger)
        return ''
    except EmptyPage:
        print('[pic_level2_2json]:', EmptyPage)
        return ''
    jsonstr = json.dumps(list(contacts.object_list))
    # jsonstr = ''
    return jsonstr


# def upp_json():
#     dirs = UpLoadDir.objects.all()
#     jsonstr = json.dumps(list(dirs))
#     return jsonstr
