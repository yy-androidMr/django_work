import os

import django
# import imageio

# 设置django 环境

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MrYangServer.settings')
django.setup()
# 设置解码环境

MEDIA_TYPE = ['.mp4', '.rmvb', '.mkv']


def find_folders():
    media_root = '../../../static/media'
    # Medias.objects.all().delete()
    for root, dirs, files in os.walk(media_root):
        for file in files:
            rela_path = os.path.join(root, file)
            if file.endswith('.mp4'):
                nginx_path = rela_path[len(media_root) + 1:]
                # nginx_path = urllib.parse.quote(nginx_path)// 不加码.在html里面加
                # media = Medias()
                # # 获取文件名
                # media.showname = file
                #
                # media.nginxPath = nginx_path
                #
                # fsize = os.path.getsize(rela_path)
                # media.moveLength = utils.sizeConvert(fsize)
                # media.movetime = ''
                # media.save()
                print('add media:%s' % rela_path)
                # encode_rela_path = rela_path.encode(encoding='UTF-8')
                # encode_rela_path.endswith()
                # encode_rela_path.endswith('.gif')
                # print(rela_path.encode(encoding='gbk'))
                # clip = VideoFileClip(rela_path.encode(encoding='gbk'))


                # print(nginx_path + ' 文件大小:' + utils.sizeConvert(fsize) + ' 视频长度:' + utils.timeConvert(rela_path))

                # file_time = self.timeConvert(clip.duration)
                # urlencode = urllib.parse.quote(rela_path)
                # print(urllib.parse.unquote(urlencode))
            else:
                print('不是媒体文件:%s' % rela_path)


if __name__ == '__main__':
    find_folders()
