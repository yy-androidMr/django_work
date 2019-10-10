# import subprocess
# out =subprocess.check_output('ping www.baidu.com',shell=True)
# print(out.decode('gbk'))
# print(decode('utf-8'))
dd = {1: 2, 2: 3, 3: 4}
ks = list(dd.keys())
for key in ks:
    del dd[key]
print(dd)
