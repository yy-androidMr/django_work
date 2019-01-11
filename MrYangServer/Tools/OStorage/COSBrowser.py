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
sys.path.append('../../')
from qcloud_cos import CosConfig, CosS3Client
from frames import yutils, ypath, logger

down_host = 'https://mryang-1251808344.cos.ap-chengdu.myqcloud.com/'
upload_list_path = 'out/upload_list.txt'
delete_list_path = 'out/delete_list.txt'
test_bucket_bat = 'bucket_test_bg.bat'
main_bucket_bat = 'bucket_main.bat'


# 同步操作.分3个步骤
# 1.配置本地文件路径
#     local_pre_path = 'E:/cache/root/'
#     localpath = 'ttt/'
#     bucketpath = 'ttt/'
# 2.执行create_diff_list获取两列表之间的差距.并且去当前的out目录确认
# 3.确认完毕执行sync_to_os,如果有问题的文件,手动操作
# 注意事项:test_bucket_bat  需要一致


# ----------------功能1--------------------
def local_list(path):
    list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '.DS_Store' in file:
                continue
            temp = ypath.join(root, file)
            size = os.path.getsize(temp)
            list.append('%s|%d' % (temp.replace(path, ''), size))
    return list


def org_os_list(cmd_res):
    org = []
    for i in cmd_res:
        i = i.strip()
        span = i.split()
        key = span[0].replace(bucket_dir, '').strip()
        if key == '/':
            continue
        size = span[1].strip()
        item = key + '|' + size
        org.append(item)
    return org


def list_finish(res, _):
    logger.info('list os files suc! do next:save different list to file! out/upload_list.txt & out/delete_list.txt')
    os_list = org_os_list(res)
    local_files = local_list(local_path)
    upload_list, delete_list = diff_path(os_list, local_files)
    upload_path = []
    for upload_item in upload_list:
        upload_path.append(local_path + upload_item.split('|')[0])

    delete_px_list = []
    for delete_item in delete_list:
        if delete_item.split('|')[0] not in upload_path:
            delete_px_list.append(bucket_dir + delete_item.split('|')[0])

    yutils.create_dirs(upload_list_path)
    with open(upload_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(upload_path))

    yutils.create_dirs(delete_list_path)
    with open(delete_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(delete_px_list))
    print(upload_list, delete_px_list)
    # print(str)


def print_diff_list(res, param):
    logger.info('bucket suc! do next:list os files')
    yutils.process_cmd('coscmd list -ar ' + bucket_dir, done_call=list_finish)


def diff_path(list_left, list_right):
    right_not_exist = list(set(list_left).difference(set(list_right)))
    left_not_exist = list(set(list_right).difference(set(list_left)))
    return left_not_exist, right_not_exist


# 先调用这个生成比对结果文件
def create_diff_list(bat):
    if not yutils.is_win():
        with open(bat, 'r') as f:
            yutils.process_cmd(f.readline(), done_call=print_diff_list)
    else:
        yutils.process_cmd(bat, done_call=print_diff_list)


# ---------------功能1结束------------------------

# ---------------功能2---------------------------
def sync_path(_, param):
    # 上传列表需要优化.一两张不需要处理成这样吧? 2000+文件上传需要几分钟 1w? 10分钟?
    yutils.process_cmd('coscmd upload -rs %s %s' % (local_path, bucket_dir))
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
    with open(upload_list_path, 'r') as f:
        can_upload = len(f.readlines()) > 0
    if can_upload and os.path.exists(upload_list_path):
        yutils.process_cmd(bat, done_call=sync_path)
    else:
        print('没有要上传的文件!')

    if os.path.exists(delete_list_path):
        # 执行批量删除
        delete_list_obj = []
        with open(delete_list_path, 'r', encoding='utf-8') as f:
            delete_list = f.readlines()
            for line in delete_list:
                delete_list_obj.append({'Key': line.split('|')[0]})
            print(delete_list_obj)
        if len(delete_list_obj) > 0:
            client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Object': delete_list_obj
                }
            )
        else:
            print('没有要删除的文件!')


# ---------------功能2结束------------------------


# ---------------功能3开始------------------------
def download(list):
    for item in list:
        url = down_host + item  # .replace(bucket_dir, '')
        local = local_path + item.replace(bucket_dir, '')
        print(url, local)
        # urllib.urlretrieve()
        # print(sync_path)


def all_download(res, _):
    for item in res:
        sync_path.append(item.strip().split()[0])
    download(sync_path)


def download_oncos():
    yutils.process_cmd('coscmd list -ar ' + bucket_dir, done_call=download)


# 示例: python3 COSBrowser.py -l /Users/mr.yang/Documents/cache/ttt -b ttt
if __name__ == '__main__':
    from frames.xml import XMLPic

    pic_cfg = XMLPic.get_infos()

    local_path = ypath.desc()
    local_path = ypath.join(local_path, pic_cfg.dir_root)
    bucket_dir = '/res/pic'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:b:c:', ['local=', 'bucket=', 'cmdf='])
    except getopt.GetoptError as e:
        print('参数错误!:' + e)
    for o, a in opts:
        if o in ('-l', '--local'):
            # print('o:' + o + '  a:' + a)
            if a.endswith('/') or a.endswith('\\'):
                a = a[:-1]
            local_path = a
        if o in ('-b', '--bucket'):
            print(a)
            if a.endswith('/') or a.endswith('\\'):
                a = a[:-1]
            bucket_dir = a

    # local_path = r'/Users/mryang/Documents/res/src/pic/thum'
    # 这是两步操作,通常需要分开
    create_diff_list(main_bucket_bat)
    print(local_path, bucket_dir)
    if yutils.is_win():
        os.system(upload_list_path)
        os.system(delete_list_path)
    else:
        os.system('open ' + upload_list_path)
        os.system('open ' + delete_list_path)
    action = input('去确认上传和下载文件吧!:(s[正常同步]|n[取消操作]|ud[把本地缺失的更新,delete_list.txt的文件会被同步到本地]):\n')
    if action == 'y':
        print('确认')
        sync_to_os(main_bucket_bat)
    if action == 'ud':
        print('同步本地缺失')
        sync_path = []
        with open(delete_list_path, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                download(lines)
            else:
                print('没有需要同步的文件')
    else:
        print('取消')
