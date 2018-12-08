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

import yy_utils

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

upload_list_path = 'out/upload_list.txt'
delete_list_path = 'out/delete_list.txt'
test_bucket_bat = 'bucket_test_bg.bat'

local_pre_path = 'E:/cache/root/'
localpath = 'ttt/'
bucketpath = 'ttt/'


# 同步操作.分3个步骤
# 1.配置本地文件路径
#     local_pre_path = 'E:/cache/root/'
#     localpath = 'ttt/'
#     bucketpath = 'ttt/'
# 2.执行diff_path获取两列表之间的差距.并且去当前的out目录确认
# 3.执行sync


def local_list(pre_path, sync_local_path):
    list = []
    for root, dirs, files in os.walk(pre_path + sync_local_path):
        for file in files:
            temp = os.path.join(root, file).replace('\\', '/')
            size = os.path.getsize(temp)
            list.append('%s|%d' % (temp.replace(pre_path, ''), size))
    return list


def org_os_list(cmd_res):
    org = []
    for i in cmd_res:
        temp_split = i.strip().split()
        item = temp_split[0] + '|' + temp_split[1]
        org.append(item)
    return org


def list_finish(res, _):
    logging.info('list os files suc! do next:save different list to file! out/upload_list.txt & out/delete_list.txt')
    os_list = org_os_list(res)
    local_files = local_list(local_pre_path, localpath)
    upload_list, delete_list = diff_path(os_list, local_files)

    yy_utils.create_dirs(upload_list_path)
    with open(upload_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(upload_list))

    yy_utils.create_dirs(delete_list_path)
    with open(delete_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(upload_list))
    print(upload_list, delete_list)
    # print(str)


def print_diff_list(res, param):
    logging.info('bucket suc! do next:list os files')
    yy_utils.process_cmd('coscmd list -ar ' + bucketpath, done_call=list_finish)


def sync_bucket(bucket_name, done_call):
    logging.info(str(bucket_name) + ' and call :' + str(done_call))
    yy_utils.process_cmd(bucket_name, done_call=done_call)


def diff_path(list_left, list_right):
    right_not_exist = list(set(list_left).difference(set(list_right)))
    left_not_exist = list(set(list_right).difference(set(list_left)))
    return left_not_exist, right_not_exist


sync_bucket(test_bucket_bat, print_diff_list)




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
