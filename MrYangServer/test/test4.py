# import subprocess
# out =subprocess.check_output('ping www.baidu.com',shell=True)
# print(out.decode('gbk'))
# print(decode('utf-8'))
import os
from pathlib import Path
# def sort_key()
from functools import cmp_to_key

mp4_ext = '.mp4'


def cmp_new(x, y):
    if x.suffix == mp4_ext:
        if y.suffix == mp4_ext:
            return -1 if x.cwd() > y.cwd() else 1
        return -1
    else:
        if y.suffix == mp4_ext:
            return 1
        else:
            return -1 if x.cwd() > y.cwd() else 1

from sys import getsizeof
sss = sorted(Path(r'Y:\src\media').rglob('*.*'), key=cmp_to_key(cmp_new))
print(getsizeof(sss))
# for li in Path(r'F:\cache\mulit\src\s1\media').rglob('*.*'):
#     print(li)
