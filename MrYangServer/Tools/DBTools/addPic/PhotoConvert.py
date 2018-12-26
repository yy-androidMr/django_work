from frames import yutils, ypath, TmpUtil
from Mryang_Tdb.models import Dir

# src->middle->thum
from frames.xml import XMLPic

pic_cfg = XMLPic.get_infos()


def insert_db(dir_list, file_list):
    dir_id = 0
    dir_db_list = {}
    for item in dir_list:
        infos = item[1]
        abs_path = item[0]
        d_model = Dir()
        d_model.name = infos[ypath.KEYS.NAME]
        # d_model.tags = name.split()
        d_model.isdir = infos[ypath.KEYS.IS_DIR]
        d_model.abs_path = abs_path  # 如果数据过大可以考虑不要
        d_model.rel_path = infos[ypath.KEYS.REL]
        d_model.type = yutils.M_FTYPE_PIC
        d_model.c_id = dir_id
        dir_id += 1

        try:
            parent = Dir.objects.get(abs_path=infos[ypath.KEYS.PARENT])
            d_model.parent_dir = parent
        except Exception as e:
            print('错误:%s:is not found :%s' % (infos[ypath.KEYS.PARENT], e))
            pass
        d_model.save()
        dir_db_list[d_model.abs_path] = d_model

    file_dirdb_list = []
    for item in file_list:
        infos = item[1]
        abs_path = item[0]
        d_model = Dir()
        d_model.name = infos[ypath.KEYS.NAME]
        d_model.isdir = infos[ypath.KEYS.IS_DIR]
        d_model.abs_path = abs_path
        d_model.rel_path = infos[ypath.KEYS.REL]
        d_model.type = yutils.M_FTYPE_PIC

        d_model.parent_dir = dir_db_list[infos[ypath.KEYS.PARENT]]
        d_model.c_id = dir_id  # 照片id为文件夹*100??存疑
        dir_id += 1

        file_dirdb_list.append(d_model)
    return file_dirdb_list


if __name__ == '__main__':

    Dir.objects.filter(type=yutils.M_FTYPE_PIC).delete()
    desc = TmpUtil.get(yutils.RESOURCE_DESC_KEY)
    desc = ypath.join(desc, pic_cfg[XMLPic.TAGS.DIR_ROOT])

    dict = ypath.path_result(desc, pic_cfg[XMLPic.TAGS.THUM], add_root=False)

    dir_dict = {}
    file_dict = {}
    for key in dict:
        if (dict[key][ypath.KEYS.IS_DIR]):
            dir_dict[key] = dict[key]
        else:
            file_dict[key] = dict[key]

    dir_list = sorted(dir_dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])
    file_list = sorted(file_dict.items(), key=lambda d: d[1][ypath.KEYS.LEVEL])

    file_db_list = insert_db(dir_list, file_list)
    Dir.objects.bulk_create(file_db_list)
