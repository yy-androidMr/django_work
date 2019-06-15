import os
from pathlib import Path


def rep(str):
    return str.replace('\\', '/')


def join(l, r):
    return rep(os.path.join(l, r))


def releative_list(path):
    path = rep(path)
    res = []
    for root, dirs, files in os.walk(path):
        res.extend([join(root, file).replace(path, '') for file in files])
    return res


def compair(folder1, folder2):
    res1_releative = releative_list(folder1)
    res2_releative = releative_list(folder2)
    # folder1_path = Path(folder1)
    # folder1_all_file = folder1_path.rglob('*')
    # folder1_posix_str = str(folder1_path.as_posix())
    # res1_releative = [folder1_path_item.as_posix().replace(folder1_posix_str, '') for folder1_path_item in
    #                   folder1_all_file]
    # tv\知否\ZF知否应是绿肥红瘦-30.mp4
    # res1_releative = [folder1_path_item.relative_to(folder1_path) for folder1_path_item in folder1_all_file]

    # folder2_path = Path(folder2)
    # folder2_all_file = folder2_path.rglob('*')
    # folder2_posix_str = str(folder1_path.as_posix())
    #
    # res2_releative = [folder2_path_item.relative_to(folder2_path) for folder2_path_item in folder2_all_file]

    res1_set = set(res1_releative)
    res2_set = set(res2_releative)
    diff = res1_set.difference(res2_set)
    for dif_item in diff:
        print(dif_item)
    # for res_file in res_releative:
    #     print(type(res_file))


# compair('Z:\src\media', 'Z:\desc\media')
compair(r'Z:\desc\media', r'Z:\src\media')
