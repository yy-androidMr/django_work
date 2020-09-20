from PIL import Image
# im = Image.open(r"W:\数据备份\其他\7.5 TJ9342 杨煜 娄敏慧 4T 8000 韩毅 妍熙 312P\正片\1\DSC07411.jpg")
# im.save("beauty.jpg")

import os
# dir = r"W:\数据备份\其他\7.5 TJ9342 杨煜 娄敏慧 4T 8000 韩毅 妍熙 312P\正片\1"
# list = os.listdir(dir)
# index = 0
# middle_area = 1600*1600
# for item in list:
#     print(item)
#     if(item.endswith(".jpg") or item.endswith(".png")):
#         im = Image.open(dir+"\\"+item)
#         # 压缩尺寸
#         w, h = im.size
#         pic_area = w * h
#         if pic_area > middle_area:
#             proportion = (middle_area / pic_area) ** 0.5
#             w = int(w * proportion)
#             h = int(h * proportion)
#         im.thumbnail((w, h), Image.ANTIALIAS)
#         im.save(r"W:\数据备份\其他\7.5 TJ9342 杨煜 娄敏慧 4T 8000 韩毅 妍熙 312P\正片\压缩后\\"+item)
#         print("处理进度："+ str(index) + "/"+ str(len(list)))
#         index +=1

#
from_dir =  r"W:\数据备份\其他\TJ9342   娄敏慧  9-20号取件"
to_dir = r"W:\数据备份\其他\7.5 TJ9342 杨煜 娄敏慧 4T 8000 韩毅 妍熙 312P\正片\压缩后"
list = os.listdir(from_dir)
lower= []
for item in list:
    lower.append(item.lower())

list2 = os.listdir(to_dir)
print(len(list2))
for item in list2:
    if item.lower() in lower:
        print(item)
        os.remove(to_dir+"\\"+item)