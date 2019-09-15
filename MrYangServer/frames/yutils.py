import codecs
import hashlib
import locale
import platform
import random
import string
import subprocess

import imageio


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
M_FTYPE_MPATH = 4  # 这是对资源根目录的类型
# end

# 运行平台
WINDOWS = 'Windows'
MAC = 'Darwin'
LINUX = 'Linux'
#


# 路径操作

banner_pic_path = '/pic/gif_bannder.png'
upload_root = 'upload'
upload_album = ''.join([upload_root, '/album'])
upload_video = ''.join([upload_root, '/video'])


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


def fileSizeConvert(size):  # 单位换算
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
        return u'%s分%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s时%s分%s秒' % (hour, mine, second)
        return tim_srt


def is_win():
    sys_str = platform.system()
    if (sys_str == WINDOWS):
        return True
    return False


def md5_of_str(src):
    md1 = hashlib.md5()
    md1.update(src.encode("utf-8"))
    return md1.hexdigest()


def is_movie(path):
    if not any(str_ in str(path).lower() for str_ in
               ('.mp4', '.mkv', '.rmvb', '.avi', '.rm', '.mov', '.wmv', '.flv', '.aac', '.ogg', '.rm'
                )):
        return False
    return True


def get_md5_steam(file_steam):
    md5_obj = hashlib.md5()
    while True:
        d = file_steam.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    return md5


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
    if not any(str_ in path.lower() for str_ in ('.jpeg', '.jpg', 'png', 'bmp')):
        return False
    return True


def is_webp(path):
    if '.webp' in path.lower():
        return True
    return False


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
    from django.db import models
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


# 视频的工具----------------------------------------------------
# INFO_FILE = 'info'
# 如果是切片视频.文件夹是这个后缀.
# M3U8_DIR_EXTEN = '.ym3'
# M3U8_NAME = 'out.m3u8'
def video_info(src):
    vid = imageio.get_reader(src)
    # {'plugin': 'ffmpeg', 'nframes': 3460, 'ffmpeg_version': '3.2.4 built with gcc 6.3.0 (GCC)', 'fps': 15.0,
    #  'source_size': (1280, 720), 'size': (1280, 720), 'duration': 230.67000000000002}
    return vid.get_meta_data()


# end----------------------------------------------------------


# cmd命令行回调----------------------------------------------------
def process_cmd(cmd, call=None, done_call=None, param=None, sep='\r\n'):
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    cmd_str = []
    while True:
        data = ps.stdout.readline()
        if data == b'':
            if ps.poll() is not None:
                if done_call is not None:
                    done_call(cmd_str, param)
                break
        else:
            line = data.decode('utf-8')
            # print(line, end='')
            cmd_str.append(line.strip('\r\n'))
            if call is not None:
                call(line)


# end-------------------------------------------

# 默认编码
default_encode = codecs.lookup(locale.getpreferredencoding()).name


# end-------


# 裁切图片 传入宽高. 然后返回对应的坐标裁切.proportion=w/h  1代表裁切正方形
def crop_size(w, h, proportion=1):
    crop_w = (w - proportion * h) / 2
    crop_h = 0
    if crop_w < 0:
        crop_h = (h - w / proportion) / 2
        crop_w = 0
    region = (crop_w, crop_h, w - crop_w, h - crop_h)
    return region
