import hashlib
import os
import random
import sys
import time
import tracemalloc

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
f = open(r'F:\cache\res\desc\pic\middle\47c0acfe173d4e198e568e459cf38b44\2c5e89164a9093de860d1e13620a1893.jpg', 'rb')
md5_obj = hashlib.md5()
while True:
    d = f.read(8096)
    if not d:
        break
    md5_obj.update(d)
hash_code = md5_obj.hexdigest()
print(hash_code)
src_img = Image.open(f)
print(src_img.size)
# f.close()
# md5 = str(hash_code).lower()
