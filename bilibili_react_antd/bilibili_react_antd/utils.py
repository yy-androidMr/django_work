import hashlib
import time
# from django.core.cache import cache

from django.core import signing
# from django_redis import get_redis_connection
# from django.core.cache import cache
# conn = get_redis_connection("default")
import pickle

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'Mr.yang'
SALT = 'www.mryang.com'
TIME_OUT = 7 * 24 * 60 * 60  # 1week


def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    print(type(raw))
    return raw


def create_token(username):
    """生成token信息"""
    # 1. 加密头信息
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload = {"username": username, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    # 存储到缓存中
    # cache.set(username, token, TIME_OUT)
    # cache.set(username, token, TIME_OUT)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


# 通过token获取用户名
def get_username(token):
    payload = get_payload(token)
    return payload['username']
    pass


def check_token(token):
    if token is None or token is '':
        return False
    username = get_username(token)
    if username:
        return True
    # last_token = cache.get(username)
    # if last_token:
    #     return last_token == token
    return False

