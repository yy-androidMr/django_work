# coding=utf-8
# doc
# https://cloud.tencent.com/document/product/436/12270
from qcloud_cos import CosConfig, CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.info('asdfsdaf')
secret_id = 'AKIDWjwhVnyiSSoAnJo8m9MNYHomrchWLJZM'  # 替换为用户的 secretId
secret_key = 'RKcdvzKz0iOO167JYiEmRIb80gC6gDzk'  # 替换为用户的 secretKey
region = 'ap-chengdu'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def upload():
    file_name = 'test.txt'
    with open('test.txt', 'rb') as fp:
        response = client.put_object(
            Bucket='mryang-1251808344',
            Body=fp,
            Key=file_name,
            StorageClass='STANDARD',
            ContentType='text/html; charset=utf-8'
        )
    print(response['ETag'])


def upload_dir():
    response = client.put_object_from_local_file(
        Bucket='mryang-1251808344',
        LocalFilePath='local.txt',
        Key=u'G:\pyWorkspace\django_work\pyHelper\OStorage\ttt',
    )
    print(response['ETag'])


upload_dir()
