import hashlib
import os

import stat

def get_md5(file_path):
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5

def delrepeat_file_list(dir_list, max_size: int = 0):
    repeat_file = {}
    md5_list = {}
    for dir in dir_list:
        print('查重该目录:' + dir)
        for root, dirs, files in os.walk(dir):
            for file in files:
                source_rela_path = os.path.join(root, file)
                if max_size != 0:
                    if os.stat(source_rela_path).st_size > max_size:
                        continue
                file_md5 = get_md5(source_rela_path)
                if file_md5 in md5_list:
                    repeat_file[source_rela_path] = md5_list[file_md5]
                    print('找到重复:' + md5_list[file_md5])
                else:
                    md5_list[file_md5] = os.path.abspath(source_rela_path)
        cmd = input('是否确认删除该目录下的重复文件?\n')
        if(cmd == 'y'):
            for file in repeat_file:
                if os.path.exists(file):
                    os.chmod(file, stat.S_IWRITE)
                    os.remove(file)
        else:
            print('不处理该路径:'+dir)
    print('delrepeat_file done')


paths = []
while True:
    path = input('输入路径{不输入路径则继续}:')
    if path is None or len(path) == 0:
        print('开始去重中...')
        break
    if (os.path.exists(path)):
        print('添加路径成功')
        paths.append(path)
    delrepeat_file_list(paths)
