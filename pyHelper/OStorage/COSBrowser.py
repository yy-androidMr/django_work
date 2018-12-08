# coding=utf-8
# api文档
# https://cloud.tencent.com/document/product/436/12270
# coscmd的文档
# https://cloud.tencent.com/document/product/436/10976?_ga=1.131638927.1487042974.1543821505

# ------------------coscmd

# pip install coscmd

# coscmd  config [-h] -a <SECRET_ID> -s <SECRET_KEY> -b <BUCKET> -r <REGION>

# -r 上传文件夹 -s同步目录和md5不会重复上传  a/b本地目录  c/ 创建c/b/目录(创建的是指定目录的最后一个文件夹中的所有文件)
# --ignore *.txt,*.doc 可选忽略
# coscmd upload -rs a/b c/

# 删除文件或者文件夹, -r 代表文件夹 -f代表不用确定  a/ 要删除的目录.
# coscmd delete -rf a/
# --------------------------
import os
from qcloud_cos import CosConfig, CosS3Client
import sys
import logging

from OStorage.ThreadingPool import ThreadingPool

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDWjwhVnyiSSoAnJo8m9MNYHomrchWLJZM'  # 替换为用户的 secretId
secret_key = 'RKcdvzKz0iOO167JYiEmRIb80gC6gDzk'  # 替换为用户的 secretKey
region = 'ap-beijing'  # 替换为用户的 Region
region2 = 'ap-chengdu'  # 替换为用户的 Region
bucket = 'mryang-bj-1251808344'
bucke2 = 'mryang-1251808344'
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
config2 = CosConfig(Region=region2, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config2)

local_pre_path = 'E:/cache/root/'
localpath = 'ttt/'
bucketpath = 'ttt/'

# 同步操作.分3个步骤
# 1.配置本地文件路径
#     local_pre_path = 'E:/cache/root/'
#     localpath = 'ttt/'
#     bucketpath = 'ttt/'
# 2.执行diff_path获取两列表之间的差距.并且确认
# 3.执行sync

import subprocess


def process_cmd(cmd, call=None, done_call=None, param=None):
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    cmd_str = []
    while True:
        data = ps.stdout.readline()
        if data == b'':
            if ps.poll() is not None:
                if done_call != None:
                    done_call(cmd_str, param)
                break
        else:
            line = data.decode('utf-8')
            # print(line, end='')
            cmd_str.append(line.replace('\r\n', ''))
            if call != None:
                call(line, param)


def local_list(pre_path, sync_local_path):
    list = []
    for root, dirs, files in os.walk(pre_path + sync_local_path):
        for file in files:
            list.append(os.path.join(root, file).replace('\\', '/').replace(pre_path, ''))
    return list


def get_os_list():
    os_list = []
    with open('out.txt', 'r', encoding='gbk') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\\', '/').split('|')[0]
            os_list.append(line)
    return os_list


def org_list(list):
    org = []
    for i in list:
        item = '|'.join(i.strip().split())
        org.append(item)
    return org


def list_finish(list, _):
    with open('out.txt', 'w') as f:
        list = org_list(list)
        f.write('\n'.join(list))
        # print(str)


def config_coscmd_finish(res, param):
    process_cmd('coscmd list -ar ' + bucketpath, done_call=list_finish)


def sync_lcoal(bucket_name):
    print('bucket_name:' + bucket_name)
    process_cmd(bucket_name, done_call=config_coscmd_finish)


def diff_path(list_left, list_right):
    right_not_exist = list(set(list_left).difference(set(list_right)))
    left_not_exist = list(set(list_right).difference(set(list_left)))
    return left_not_exist, right_not_exist


os_list = get_os_list()
local_files = local_list(local_pre_path, localpath)
upload_list, delete_list = diff_path(os_list, local_files)
print(upload_list, delete_list)

# process_cmd('coscmd list -ar', call, done)


# sync_lcoal('bucket_test_bg.bat')
# strs = '   ttt/1.png                17994      2018-12-05 15:58:50   '
# print('|'.join(strs.strip().split()))
# list_objects()
# def delete_list(dict):
#     print(dict)
#
# dic = {'k1': 'v1', 'k2': 'v2'}
# dic['ttt/躲猫猫/1.png']='ttt/'
# delete_list(dic)
#
# tp = ThreadingPool()
#
# for root, dirs, files in os.walk('ttt/'):
#     for file in files:
#         source_path = os.path.join(root, file).replace('\\', '/')
#         tp.append(upload_dir, (source_path, source_path))
#         print(source_path)
#
# tp.start()

#
# tp.append(m2)
# tp.start()


# Delete = {
#     'Object': [
#         {
#             'Key': 'string',
#         },
#     ],
#     'Quiet': 'true' | 'false'
# }
