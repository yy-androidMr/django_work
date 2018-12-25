import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
from Mryang_App.models import Dir as MDir
from Mryang_Tdb.models import Dir as TDir


# 本地的dir文件,转换成sql的dir文件
def localdir2sqldir():
    data_list = list(MDir.objects.all())
    out_list = {}
    sql_data_list = []
    for item in data_list:
        td = TDir()
        td.id = item.id
        td.name = item.name
        # td.parent_dir = item.parent_dir
        td.isdir = item.isdir
        td.tags = item.tags
        td.abs_path = item.abs_path
        td.rel_path = item.rel_path
        td.type = item.type
        td.c_id = item.c_id
        out_list[td.id] = (td, item.parent_dir_id)
        sql_data_list.append(td)

    for out_key in out_list:
        td, parent_dir_id = out_list[out_key]
        if parent_dir_id:
            p_td, _ = out_list[parent_dir_id]
            td.parent_dir = p_td
    TDir.objects.bulk_create(sql_data_list)
