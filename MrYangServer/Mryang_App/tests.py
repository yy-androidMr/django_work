# coding:utf-8

import sys, django, os

proj_abs_path = os.path.abspath(os.path.join(sys.argv[0], '../..'))
sys.path.append(proj_abs_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()

# Create your tests here.
from frames.yutils import *

user_list = {'tk1': 'yy', 'tk2': 'wwjt', 'tk3': 'dd', 'tk4': '44ss', 'tk5': 'zzz', 'tk6': 'bb'}


def create_user():
    for _token in user_list:
        user, created = User.objects.get_or_create(token=_token)
        if created:
            name_value = user_list.get(_token)
            print('created:%s,value:%s' % (created, name_value))
            # if created:
            user.user_name = name_value
            user.account = random_int()
            user.pwd = random_str()
            user.save()
        else:
            print('该token已被创建:%s' % _token)


def main():
    create_user()


class A():
    def __str__(self):
        return 'a'


# if __name__ == '__main__':
#     print(A())
#     main()
#     print('done!:')

import base64


def baseurl(url):

    if url.startswith('thunder://'):
        url = url[10:] + '\n'
        url = base64.decodestring(url)
        url = url[2:-2]
    elif url.startswith('flashget://'):
        url = url[11:url.find('&')] + '\n'
        url = base64.decodestring(url)
        url = url[10:-10]
    elif url.startswith('qqdl://'):
        url = url[7:] + '\n'
        url = base64.decodestring(url)
    else:
        print('\n It is not a available url!!')
    return url


# www.iplaypy.com

def test():
    url = 'thunder://QUFmdHA6Ly95Z2R5ODp5Z2R5OEB5ZzQ1LmR5ZHl0dC5uZXQ6NzA5Mi9bJUU5JTk4JUIzJUU1JTg1JTg5JUU3JTk0JUI1JUU1JUJEJUIxd3d3LnlnZHk4Lm5ldF0uJUU4JThCJUIxbHVuJUU1JUFGJUI5JUU1JTg2JUIzLkhELjcyMHAuJUU1JTlCJUJEJUU4JThCJUIxJUU1JThGJThDJUU4JUFGJUFELiVFNCVCOCVBRCVFOCU4QiVCMSVFNSU4RiU4QyVFNSVBRCU5NyVFNSVCOSU5NS5ta3ZaWg=='
    p = baseurl(url)
    print('\n============请将下面地址复制到你的下载器中=============\n')
    print(p)


if __name__ == '__main__':
    print(base64.b64encode('红楼梦小戏骨'))