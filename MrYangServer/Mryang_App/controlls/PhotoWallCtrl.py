import json
import os
import threading

from django.db import transaction
from django.db.models import F

from Mryang_App.models import Dir, PhotoWall, Photo
from frames import yutils


def batch_create_on_dir():
    dir_query = Dir.objects.filter(type=yutils.M_FTYPE_PIC)
    dir_names = []
    for dir_db in dir_query:
        if dir_db.parent_dir == None:
            continue
        dir_names.append(os.path.basename(dir_db.rel_path))
        # if dir_db.rel_path:
    pw_query = PhotoWall.objects.all()
    for pw_db in pw_query:
        try:
            dir_names.remove(pw_db.name)
        except:
            pass
    print(dir_names)
    pw_create_list = []
    for d_name in dir_names:
        pw_db = PhotoWall()
        pw_db.nick = pw_db.name = d_name
        pw_create_list.append(pw_db)
    if len(pw_create_list) > 0:
        PhotoWall.objects.bulk_create(pw_create_list)
        return json.dumps({1: '转换成功'})
    return json.dumps({2: '没有可以转换的目标'})


in_sync_photo = False
lock = threading.Lock()


def batch_photo_to_wall():
    global in_sync_photo

    def begin():
        batch_create_on_dir()
        pw_query = PhotoWall.objects.all()
        dir_names = {}
        for pw_db in pw_query:
            dir_names[pw_db.name] = pw_db
        with transaction.atomic():
            for p in Photo.objects.all():
                if p.photo_wall_id == None:
                    wall_name = os.path.basename(os.path.dirname(p.src_abs_path))
                    if wall_name in dir_names:
                        p.photo_wall_id = dir_names[wall_name].id
                        p.save()
                        # 将没有归类的图片自动归类.
        with transaction.atomic():
            for item in dir_names:
                if dir_names[item].thum_photo == None:
                    dir_names[item].thum_photo = Photo.objects.filter(photo_wall_id=dir_names[item].id).first()
                    dir_names[item].save()
        global in_sync_photo
        in_sync_photo = False

    with lock:
        if in_sync_photo:
            return json.dumps({2: '正在转换,请稍等'})
    in_sync_photo = True

    threading.Thread(target=begin).start()
    return json.dumps({1: '正在后台同步'})


def photo_wall_list(show_level):
    pw_query = PhotoWall.objects.filter(level__lt=show_level + 1, hidden=False).annotate(
        photo_path=F('thum_photo__desc_rela_path'), mpath=F('thum_photo__desc_mpath__param1')).values('nick', 'id',
                                                                                                      'intro', 'time',
                                                                                                      'level',
                                                                                                      'photo_path',
                                                                                                      'mpath')
    return json.dumps(list(pw_query))


def photo_list(wall_id):
    pl_query = Photo.objects.filter(photo_wall_id=wall_id).values('desc_rela_path')
    return json.dumps(list(pl_query))
