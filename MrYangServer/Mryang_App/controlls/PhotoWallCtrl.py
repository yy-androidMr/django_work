from Mryang_App.models import Dir
from frames import yutils


def batch_create_on_dir():
    dir_query = Dir.objects.filter(type=yutils.M_FTYPE_PIC, parent_dir=None)
    for dir_db in dir_query:
        print(dir_db.rel_path)
    return [dir_db.rel_path for dir_db in dir_query]
