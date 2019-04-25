import os
import pickle

from frames import yutils, ypath, TmpUtil


# 做步骤处理时的缓存. 某一个步骤锁
class CacheTmpInfo:
    def __init__(self):
        self.info_dic = {}
        self.tmp_file_dict = {}

    def tmp_info(self, path):
        self.init_path(path)
        return self.info_dic[path]

    def write_info(self, path, k, v):
        self.init_path(path)
        with open(self.tmp_file_dict[path], 'wb') as file:
            self.info_dic[path][k] = v
            pickle.dump(self.info_dic[path], file)
            file.close()

    def init_path(self, path):
        if not self.tmp_file_dict.get(path):
            self.tmp_file_dict[path] = ypath.join(TmpUtil.desc_tmp(), yutils.md5_of_str(path))

        if not self.info_dic.get(path):
            if not os.path.exists(self.tmp_file_dict[path]):
                self.info_dic[path] = {}
            else:
                file = open(self.tmp_file_dict[path], 'rb')
                self.info_dic[path] = pickle.load(file)
