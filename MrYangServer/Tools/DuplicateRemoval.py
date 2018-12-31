# 文件去重工作.
import os

from frames import yutils


# 删除所有文件中 有重复的图.
def delfile(path):
    print(path)
    repeat_file = {}
    for root, dirs, files in os.walk(path):
        md5_list = {}
        for file in files:
            source_rela_path = os.path.join(root, file)
            file_md5 = yutils.get_md5(source_rela_path)
            if file_md5 in md5_list:
                repeat_file[source_rela_path] = md5_list[file_md5]
            else:
                md5_list[file_md5] = os.path.abspath(source_rela_path)
        print('next')
    print(repeat_file)
    for file in repeat_file:
        print(file)
        os.remove(file)
    print('done')


delfile(r"E:\resource\src\movie")
# delfile('F:\django_work\MrYangServer\media_source\pic\src\朋友')
