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

Image.open(r'D:\cache\4\1.png').save(r'D:\cache\4\1.webp','webp')

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
