import os

import yy_utils
from tomorrow import threads

m3u8_file = 'playlist.m3u8'
ts_ext = '.ts'


#
def download_m3u8(m3u8_url, target_dir):
    u8_file = os.path.join(target_dir, m3u8_file)
    yy_utils.download(m3u8_url, u8_file)
    return u8_file


def down_ts(m3u8_file, u8_url):
    u8_dir = os.path.dirname(m3u8_file)
    u8_url_pre = os.path.dirname(u8_url)
    with open(os.path.join(m3u8_file, m3u8_file), 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if not ts_ext in line:
                continue
            line = line.strip()
            yy_utils.async_download(u8_url_pre + '/' + line, os.path.join(u8_dir, line.strip()))
            # print(line)


# local_m3 = download_m3u8('https://videos4.jsyunbf.com/2018/12/11/k4MTPAntpWxEaCjP/playlist.m3u8', r'F:\cache\毒液')
down_ts(os.path.join(r'F:\cache\毒液', m3u8_file),
        'https://videos4.jsyunbf.com/2018/12/11/k4MTPAntpWxEaCjP/playlist.m3u8')

print("finish!!!!")
# 再用如下命令合成
# ffmpeg - i
# # http: // ...
# # m3u8 - c
# # copy
# # out.mkv
