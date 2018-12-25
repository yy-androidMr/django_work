import os
import django

# 设置django 环境
from Mryang_App.models import Dir
from frames.xml import XMLMovie, XMLBase
from frames import ypath, yutils

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()

movie_config = XMLMovie.get_infos()


# 插入数据库
def insert_db(path, info):
    name = info[ypath.KEYS.NAME]
    parent_path = info[ypath.KEYS.PARENT]
    rel_path = info[ypath.KEYS.REL]
    is_dir = True
    if movie_config[XMLMovie.TAGS.DIR_EXTEN] in name:
        is_dir = False

    d_model = Dir()
    d_model.name = name
    d_model.isdir = is_dir
    d_model.abs_path = path
    d_model.rel_path = rel_path
    d_model.type = yutils.M_FTYPE_MOIVE
    try:
        parent = Dir.objects.get(abs_path=parent_path)
        d_model.parent_dir = parent
    except Exception as e:
        print('错误:%s:is not found :%s' % (parent_path, e))
        pass
    d_model.save()


if __name__ == '__main__':
    res_root, _ = XMLBase.resource_root()

    Dir.objects.filter(type=yutils.M_FTYPE_MOIVE).delete()
    dict = ypath.path_result(res_root, movie_config[XMLMovie.TAGS.DIR_ROOT], parse_file=False)

    list = sorted(dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])
    for item in list:
        insert_db(item[0], item[1])
