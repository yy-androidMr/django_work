# -*- coding: utf-8 -*-
import hashlib
import os
import random
import shutil
import sys
import time
import tracemalloc

import piexif
from PIL import Image, ImageDraw, ImageFont

#
# im2 = Image.open(r'D:\python\django_work\res_link\src\pic\webp_test.png')
# print(im2.tell())
# print(im2.format)
# im2 = Image.open(r'D:\python\django_work\res_link\src\pic\map234.jpg')
# print(im2.tell())
# print(im2.format)
# im = Image.open(r'D:\python\django_work\res_link\src\pic\test_gif.gif')
# im = im.convert("RGB")
# draw = ImageDraw.Draw(im)
# font = ImageFont.truetype("arial.ttf", 40, encoding="unic")  # 设置字体
# draw.text((0, 0), u'GIF', font=font)
#
# im.save(r'D:\python\django_work\res_link\src\pic\test_gif222.jpg')


# im = Image.open(r'D:\python\django_work\res_link\src\pic\test_gif.gif')
# im.save(r'D:\python\django_work\res_link\src\pic\test_gif222.webp')

# Image.open(r'D:\cache\4\1.png').save(r'D:\cache\4\1.webp','webp')

# im = Image.open(r'D:\python\django_work\res_link\src\pic\test_gif222.webp')
# im.save(r'D:\python\django_work\res_link\src\pic\test_gif222.jpg')
#
# # im.mode = "PNG"
# im.save(r'D:\python\django_work\res_link\src\pic\picframe00.png'.format(im.tell()), "JPEG")
# im = Image.open(r'D:\python\django_work\res_link\src\pic\picframe00.png')
# im = im.convert('RGB')
# im.save(r'D:\python\django_work\res_link\src\pic\picframe00.jpg')
#
# print(im.format)
# im.save(r'D:\python\django_work\res_link\src\pic\picframe00_.jpg')
# print(im.mode)
# im.save(r'D:\python\django_work\res_link\src\pic\test_gif.webp')
# im2 = Image.open(r'D:\python\django_work\res_link\src\pic\test_gif.webp')
# if im2.mode == 'RGBA':
#     im.save(r'D:\python\django_work\res_link\src\pic\test_gif2.png')
#
# else:
#     im.save(r'D:\python\django_work\res_link\src\pic\test_gif2.jpg')

# print(hex(0x153b2f3518469ddac257eeef9feb1f55))
#
# print('D:/cache/res/src/pic/Group/Image1/)588Q%6H%R8S8XC$$)5IR}9.jpg'> 'D:/cache/res/src/pic/Group/)588Q%6H%R8S8XC$$)5IR}9.jpg')
# pi = PicInfo()
# pi.size = (0x153b2f3518469ddac257eeef9feb1f55)
# pi.gallery_key_id = 5
# pi.save()

# print(0x153b2f3518469ddac257eeef9feb1f55)
# from frames import yutils
#
# file_md5 = yutils.get_md5(r'D:\cache\res\src\pic\Group\)588Q%6H%R8S8XC$$)5IR}9.jpg')
# file_md52 = yutils.get_md5(r'D:\cache\res\src\pic\Group\Image1\)588Q%6H%R8S8XC$$)5IR}9.jpg')
# print(file_md5)

# mm = {}
# mm['a'] = 1
# print(mm)
#
# mm['a'] = 2
# print(mm)
# print(os.path.dirname('C:/a/b'))
# import djangos

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrYangServer.settings")
# django.setup()
#
# md1 = hashlib.md5()
# md1.update('.'.encode("utf-8"))
# print(md1.hexdigest())
# print(sys.maxsize)
# Dir.objects.all().delete()
# m_list = list(m_list)
# tm = TestMode.objects.create()
# tm.folder_key.add(m_list[0])
# tm.save()
# f.close()
# for root, dirs, files in os.walk(r'D:\\'):
#     for file in files:
#         if os.stat(os.path.join(root, file)).st_ctime_ns < 1062510500751:
#             print(os.path.join(root, file))
# from frames import yutils

#
# print(time.time())
# for i in range(1000*100):
#     file_md5 = yutils.get_md5(r"C:\Users\Administrator\Desktop\game\云顶之弈.jpg")
# print(time.time())

# print(file_md5)


# yutils.file_fingerprint(r"C:\Users\Administrator\Desktop\game\云顶之弈.jpg")
# sss = os.stat(r"C:\Users\Administrator\Desktop\game\云顶之弈.jpg")
# timeStruct = time.localtime(int(sss.st_ctime))
# # tm_year
# # tm_mon
# print(int(sss.st_ctime) % 1000)
# os.symlink(r'D:\README.en.md', r'D:\README2.en.md')
# print(os.path.getctime(r'D:\README2.en.md'))
# print(os.path.exists(r'D:\README2.en.md'))
# print(os.path.islink(r'D:\README2.en.md'))

# print(time.time())
# for i in range(100 * 1000):
#     sss =
# os.remove(r'D:/cache/mulit_dir/s2/pic\\文件夹1\\GVE周活动_结算奖励_窄屏.png')
# print(time.time())

s_img = Image.open(r'D:\cache\TouchArea\1\GVE_上周战绩_基准.png')
# pixel = s_img.load()
# w, h = s_img.size
# for i in range(w):
#     for j in range(h):
#         if pixel[i, j][3] != 255:
#             print(pixel[i, j])
# if s_img.mode == 'RGB':
#     s_img = s_img.convert('RGB')
# #     s_img.save(r'D:\cache\TouchArea\1\2.jpg')
# # else:
# s_img = s_img.convert('RGB')
s_img.save(r'D:\cache\TouchArea\1\GVE_上周战绩_基准.jpg')

# s_img.thumbnail((1920, 1080))
# s_img.save(r'D:\cache\TouchArea\1\2.png')
