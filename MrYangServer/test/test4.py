# import subprocess
# out =subprocess.check_output('ping www.baidu.com',shell=True)
# print(out.decode('gbk'))
# print(decode('utf-8'))
import os
import stat
import time

from frames import yutils, ypath

# os.utime(r'F:\cache\AutoCAD2017 for MAC\1568603151319.mp4',(1572602407,1572602407))



# ypath.delrepeat_file(r"F:\cache\照片导出")
yutils.convertWebp(r'F:\cache\照片导出')
# repeat_file = ypath.delrepeat_file_list([r"U:\数据备份",r"F:\cache\照片导出"])
# input("按任意键继续")
# for file in repeat_file:
#     if os.path.exists(file):
#         os.chmod(file, stat.S_IWRITE)
#         os.remove(file)
#