import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()

# 设置django 环境
from Mryang_App.models import Dir, MovieInfo
from frames.xml import XMLMovie, XMLBase
from frames import ypath, yutils

movie_config = XMLMovie.get_infos()
movie_item_config = XMLMovie.item_info_dict()


def insert_gallery_info():
    MovieInfo.objects.all().delete()

    movie_infos = Dir.objects.filter(isdir=False, type=yutils.M_FTYPE_MOIVE)
    movie_info_data = []
    for movie_info in movie_infos:
        if movie_info.rel_path and movie_info.rel_path in movie_item_config:
            m_cfg = movie_item_config[movie_info.rel_path]
            data = MovieInfo()
            data.name = m_cfg[XMLMovie.ITEM_TAGS.NAME]
            data.duration = m_cfg[XMLMovie.ITEM_TAGS.DURATION]
            data.size = m_cfg[XMLMovie.ITEM_TAGS.SIZE]
            value = tuple(eval(m_cfg[XMLMovie.ITEM_TAGS.PIXEL]))
            data.source_size = int(value[1])
            data.fps = m_cfg[XMLMovie.ITEM_TAGS.FPS]
            data.folder_key = movie_info
            movie_info_data.append(data)
            print(m_cfg)
    MovieInfo.objects.bulk_create(movie_info_data)
    print('done')


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
    from frames import TmpUtil

    desc_root = TmpUtil.get(yutils.RESOURCE_DESC_KEY)
    # 转码结束后的切片路径
    m3u8_ts_root = ypath.join(desc_root, movie_config[XMLMovie.TAGS.TS_DIR])

    Dir.objects.filter(type=yutils.M_FTYPE_MOIVE).delete()
    dict = ypath.path_result(res_root, movie_config[XMLMovie.TAGS.DIR_ROOT], parse_file=False)

    list = sorted(dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])
    for item in list:
        insert_db(item[0], item[1])

    insert_gallery_info()
