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
import getopt
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from qcloud_cos import CosConfig, CosS3Client
import logging
import re
import yy_utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

upload_list_path = 'out/upload_list.txt'
delete_list_path = 'out/delete_list.txt'
test_bucket_bat = 'bucket_test_bg.bat'
main_bucket_bat = 'bucket_main.bat'

local_pre_path = 'E:/cache/root/'
sync_local_dir = 'ttt'
bucket_dir = 'ttt'


# 同步操作.分3个步骤
# 1.配置本地文件路径
#     local_pre_path = 'E:/cache/root/'
#     localpath = 'ttt/'
#     bucketpath = 'ttt/'
# 2.执行create_diff_list获取两列表之间的差距.并且去当前的out目录确认
# 3.确认完毕执行sync_to_os,如果有问题的文件,手动操作
# 注意事项:test_bucket_bat  需要一致


# ----------------功能1--------------------
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
        i = i.strip()
        span = re.match(r'(.+) +(\d+) +\d{4}-\d{2}-\d{2}', i)
        key = span.group(1).strip()
        size = span.group(2).strip()
        item = key + '|' + size
        org.append(item)
    return org


def list_finish(res, _):
    logging.info('list os files suc! do next:save different list to file! out/upload_list.txt & out/delete_list.txt')
    os_list = org_os_list(res)
    local_files = local_list(local_pre_path, sync_local_dir)
    upload_list, delete_list = diff_path(os_list, local_files)
    upload_path = []
    for upload_item in upload_list:
        upload_path.append(upload_item.split('|')[0])

    delete_px_list = []
    for delete_item in delete_list:
        if delete_item.split('|')[0] not in upload_path:
            delete_px_list.append(delete_item)

    yy_utils.create_dirs(upload_list_path)
    with open(upload_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(upload_list))

    yy_utils.create_dirs(delete_list_path)
    with open(delete_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(delete_px_list))
    print(upload_list, delete_px_list)
    # print(str)


def print_diff_list(res, param):
    logging.info('bucket suc! do next:list os files')
    yy_utils.process_cmd('coscmd list -ar ' + bucket_dir, done_call=list_finish)


def diff_path(list_left, list_right):
    right_not_exist = list(set(list_left).difference(set(list_right)))
    left_not_exist = list(set(list_right).difference(set(list_left)))
    return left_not_exist, right_not_exist


# 先调用这个生成比对结果文件
def create_diff_list(bat):
    if yy_utils.is_mac():
        with open(bat, 'r') as f:
            yy_utils.process_cmd(f.readline(), done_call=print_diff_list)
    else:
        yy_utils.process_cmd(bat, done_call=print_diff_list)


# ---------------功能1结束------------------------

# ---------------功能2---------------------------
def sync_path(_, param):
    # 上传列表需要优化.一两张不需要处理成这样吧? 2000+文件上传需要几分钟 1w? 10分钟?
    yy_utils.process_cmd('coscmd upload -rs %s %s' % (local_pre_path + sync_local_dir, bucket_dir))
    pass


# 删除指定文件,并且同步目录即可,并不需要上传什么
def sync_to_os(bat):
    with open(bat, 'r') as f:
        cmd_line = f.readline()
        cmd_splite = cmd_line.split()
        region_index = cmd_splite.index('-r') + 1
        region = cmd_splite[region_index]
        secret_id_index = cmd_splite.index('-a') + 1
        secret_id = cmd_splite[secret_id_index]
        secret_key_index = cmd_splite.index('-s') + 1
        secret_key = cmd_splite[secret_key_index]
        bucket_index = cmd_splite.index('-b') + 1
        bucket = cmd_splite[bucket_index]
        config2 = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=None, Scheme='https')
        client = CosS3Client(config2)
    if os.path.exists(upload_list_path):
        yy_utils.process_cmd(bat, done_call=sync_path)
        pass
    if os.path.exists(delete_list_path):
        # 执行批量删除
        delete_list_obj = []
        with open(delete_list_path, 'r', encoding='utf-8') as f:
            delete_list = f.readlines()
            for line in delete_list:
                delete_list_obj.append({'Key': line.split('|')[0]})
            print(delete_list_obj)
        client.delete_objects(
            Bucket=bucket,
            Delete={
                'Object': delete_list_obj
            }
        )


# ---------------功能2结束------------------------


# 示例: python3 COSBrowser.py -l /Users/mr.yang/Documents/cache/ttt -b ttt
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:b:c:', ['local=', 'bucket=', 'cmdf='])
    except getopt.GetoptError as e:
        print('参数错误!:' + e)
    for o, a in opts:
        if o in ('-l', '--local'):
            # print('o:' + o + '  a:' + a)
            if a.endswith('/') or a.endswith('\\'):
                a = a[:-1]
            local_pre_path = os.path.dirname(a) + '/'
            sync_local_dir = os.path.basename(a)
        if o in ('-b', '--bucket'):
            print(a)
            if a.endswith('/') or a.endswith('\\'):
                a = a[:-1]
            bucket_dir = a
    bucket_dir = 'media/pic'
    sync_local_dir = r'pic'
    local_pre_path = r'E:/resource/desc/'
    print(local_pre_path, sync_local_dir, bucket_dir)
    # 这是两步操作,通常需要分开
    create_diff_list(main_bucket_bat)
    # os.system(upload_list_path)
    os.system('open ' + upload_list_path)
    os.system('open ' + delete_list_path)
    input = input('去确认上传和下载文件吧!:(y|n)')
    if (input == 'y'):
        print('确认')
        sync_to_os(main_bucket_bat)
    else:
        print('取消')
