import subprocess
print(subprocess.check_output('ping www.baidu.com',shell=True).decode('utf-8'))