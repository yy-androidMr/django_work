# coding:utf-8
import hashlib
import os
import random
import string
import platform

import shutil
from django.db import models


def random_int():
    return random.randint(10000000, 99999999)


def random_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(8, 20)))
    return salt


LOGIN_TIME_OUT = 7 * 24 * 60 * 60  # 7天失效

S_ACCOUNT = 'user_account'

S_NAME = 'user_name'

# media的文件类型.
M_FTYPE_MOIVE = 1
M_FTYPE_PIC = 2
M_FTYPE_DOC = 3


# end


def is_login(session):
    user_name = session.get(S_NAME, '')
    if user_name:
        return True
    else:
        return False


def get_s_account(session):
    act = session.get(S_ACCOUNT, '')
    return act


def logout(session):
    user_name = session.get(S_NAME)
    if user_name:
        del session[S_NAME]


def is_login_c(cookie):
    user_name = cookie.get(S_NAME, '')
    if user_name:
        return True
    else:
        return False


def get_s_account_c(cookie):
    act = cookie.get(S_ACCOUNT, '')
    return act


def print_download_prog(downloaded, bytelist, totalbyte):
    per = 100.0 * downloaded * bytelist / totalbyte
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def sizeConvert(size):  # 单位换算
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        return str(round(size / G, 1)) + 'GB'
    elif size >= M:
        return str(round(size / M, 1)) + 'MB'
    elif size >= K:
        return str(round(size / K, 1)) + 'KB'
    else:
        return str(round(size, 1)) + 'Bytes'


def time_convert(size):  # 单位换算
    M, H = 60, 60 ** 2
    if size < M:
        return str(size) + u'秒'
    if size < H:
        return u'%s分钟%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
        return tim_srt


def create_dirs(file_path, is_dir=False, delete_exist=False):
    if is_dir:
        target_dir = file_path
    else:
        target_dir = os.path.dirname(file_path)

    if target_dir:
        if os.path.exists(target_dir):
            if delete_exist:
                shutil.rmtree(target_dir)
            else:
                return
        os.makedirs(target_dir)


def delete_null_dir(dirr):
    if os.path.isdir(dirr):
        for p in os.listdir(dirr):
            d = os.path.join(dirr, p)
            if (os.path.isdir(d) == True):
                delete_null_dir(d)
    if not os.listdir(dirr):
        os.rmdir(dirr)
        print('移除空目录: ', dirr)


# 文件名
def file_name(file):
    return os.path.splitext(file)[0]


# 拓展名.
def file_exten(file):
    return os.path.splitext(file)[1]


# 路径操作
output_neighbor = False
neighbor_meida_root1 = r'\\Desktop-089j9k4\media'

media_source = 'E:/media_source'
static_root = 'F:/django_work/MrYangServer/static'

banner_pic_path = '/pic/gif_bannder.png'
static_media_root = neighbor_meida_root1 if output_neighbor else ''.join([static_root, '/media'])
upload_root = 'upload'
upload_album = ''.join([upload_root, '/album'])
upload_video = ''.join([upload_root, '/video'])


def gif_banner_path():
    source_abs_path = os.path.abspath('.')
    print(source_abs_path)


if __name__ == '__main__':
    gif_banner_path()


# 分解路径1.src的相对路径. 2.src的根目录. 3.目标的路径
def decompose_path(root, file, source_root, target_root, exten=None):
    source_rela_path = os.path.join(root, file)
    if not output_neighbor:
        target_root = target_root.replace('\\', '/').replace('//', '/')

    # 需要返回几个值:
    # 1.去掉source_root的相对路径.
    rela_file_name = source_rela_path[len(source_root):].replace('\\', '/').replace('//', '/')

    # 2.老的绝对路径
    source_abs_path = os.path.abspath(source_rela_path)
    source_abs_path = source_abs_path.replace('\\', '/').replace('//', '/')

    # 3.替换后缀
    if exten:
        rela_file_name = ''.join([os.path.splitext(rela_file_name)[0], exten])

    # 3.5改名 暂时不需要.
    # if rename:

    # 4.新的绝对路径|替换后缀
    if output_neighbor:
        target_abs_path = target_root
    else:
        target_abs_path = '/'.join([os.path.abspath(target_root), rela_file_name])
        target_abs_path = target_abs_path.replace('\\', '/').replace('//', '/')

    # 5.新相对路径|替换后缀
    target_rela_path = ''.join([target_root, rela_file_name])

    return (rela_file_name, source_abs_path, target_abs_path, target_rela_path)


# 5.所有路径标志符都换成/


def transform_path(cd_count, middle, last=''):
    if output_neighbor:
        return ''.join([middle, last])
    else:
        return ''.join([cd_count, middle, last])


# cd cout 往回倒多少个
def media_root():
    return media_source


def is_mac():
    sys_str = platform.system()
    if (sys_str == "Windows"):
        return False
    return True


def md5_of_str(src):
    md1 = hashlib.md5()
    md1.update(src.encode("utf-8"))
    return md1.hexdigest()


def is_movie(path):
    if not any(str_ in path.lower() for str_ in ('.mp4', '.mkv', '.rmvb', '.avi')):
        return False
    return True


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


def is_photo(path):
    if not any(str_ in path.lower() for str_ in ('.jpeg', '.jpg', 'png')):
        return False
    return True


def is_gif(path):
    if '.gif' in path.lower():
        return True
    return False


# 字段转换工具.
def to_dict_clear_none(ins):
    dict = to_dict(ins)
    dict_clear_none(dict)
    return dict


def dict_clear_none(dict):
    for key in list(dict.keys()):
        if not dict.get(key):
            del dict[key]
    return dict


def list_clear_none(list_value):
    for value in list_value:
        if type(value) == dict:
            dict_clear_none(value)


def to_dict(ins):
    if isinstance(ins, models.Model):
        field_attr = [f.name for f in ins._meta.fields]
        temp_dict = {}
        for attr in field_attr:
            value = getattr(ins, attr)
            if isinstance(value, models.Model):
                key_dict = to_dict(value)
                temp_dict.update(key_dict)
            else:
                temp_dict[attr] = value

                # temp_dict[attr] = value
        return temp_dict
        # return dict([(attr, getattr(ins, attr)) for attr in [f.name for f in ins._meta.fields]])
    elif type(ins) is dict:
        return ins
    else:
        return ins.__dict__


# class a:
#     def __init__(self):
#         self.b = 'a'
#
#
# aa = a()
# print(to_dict(aa))
# 视频的工具----------------------------------------------------
INFO_FILE = 'info'
# 如果是切片视频.文件夹是这个后缀.
M3U8_DIR_EXTEN = '.ym3'
M3U8_NAME = 'out.m3u8'
MOVIE_INFO_NAME = 'name'


def is_m3u8_dir(path):
    if M3U8_DIR_EXTEN in path.lower():
        return True
    return False


# end----------------------------------------------------------

# cmd命令行回调----------------------------------------------------
import subprocess
import codecs
import locale


def process_cmd(cmd, call=None, done_call=None):
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    while True:
        data = ps.stdout.readline()
        if data == b'':
            if ps.poll() is not None:
                if done_call != None:
                    done_call()
                break
        else:
            line = data.decode(codecs.lookup(locale.getpreferredencoding()).name)
            print(line, end='')
            if done_call != None:
                call(line)

# end----------------------------------------------------------
