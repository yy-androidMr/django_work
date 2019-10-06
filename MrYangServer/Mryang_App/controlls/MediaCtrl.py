import json

from django.db.models import F

from Mryang_App import DBHelper
from Mryang_App.models import Dir, Media
from frames import yutils, ypath
from frames.xml import XMLBase

movie_config = XMLBase.list_cfg_infos('media_info')  # XMLMedia.get_infos()


def meida_root(tags):
    root_dir = Dir.objects.get(tags=tags, parent_dir=None)
    return media_dir(root_dir.id)


def media_dir(p_id):
    dinfos = Dir.objects.annotate(p_id=F('parent_dir__id')).filter(type=yutils.M_FTYPE_MOIVE,
                                                                   parent_dir_id=p_id).values(
        'id', 'name')
    minfos = Media.objects.filter(src_dir_id=p_id, state=DBHelper.end_media_state()).annotate(
        mpath=F('desc_mpath__param1')).values('desc_path',
                                              'file_name',
                                              'duration',
                                              'size',
                                              'width',
                                              'height',
                                              'r_frame_rate',
                                              'mpath')
    # ress = json.dumps(list(minfos))
    # ress = json.loads(ress)
    res_infos = []
    for minfo in list(minfos):
        tmp_dict = {}
        tmp_dict['file_name'] = ypath.del_exten(minfo['file_name'])
        tmp_dict['nginx_path'] = ypath.join(minfo['mpath'], movie_config.dir_root, minfo['desc_path'])
        tmp_dict['duration'] = minfo['duration']
        tmp_dict['size'] = minfo['size']
        tmp_dict['width'] = minfo['width']
        tmp_dict['height'] = minfo['height']
        tmp_dict['r_frame_rate'] = minfo['r_frame_rate']
        tmp_dict['img'] = ypath.join(minfo['mpath'], movie_config.img_info.img_root, minfo['desc_path'],
                                     movie_config.img_info.thum)
        res_infos.append(tmp_dict)
    # res_infos =json.dumps()
    res = {'dir': list(dinfos), 'info': res_infos}
    json_res = json.dumps(res)
    return json_res
