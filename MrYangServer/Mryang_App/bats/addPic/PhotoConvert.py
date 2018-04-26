import os


def find_src():
    src_root = '../../../static/media/pic/src'
    for root, dirs, files in os.walk(src_root):
        for dir in dirs:
            source_path = os.path.join(root, dir).replace('\\', '/') + '/'
            rel_path = source_path[len(src_root):]
            # flush_dirs(source_path, rel_path, True, dir, fileType)

        for file in files:
            source_path = os.path.join(root, file).replace('\\', '/')
            rel_path = source_path[len(src_root):]
            # flush_dirs(source_path, rel_path, False, file, fileType)


def insert_pic():
    thum_root = '../../../static/media/pic/thum'
    big_root = '../../../static/media/pic/big'



    pass




if __name__ == '__main__':
    pass
