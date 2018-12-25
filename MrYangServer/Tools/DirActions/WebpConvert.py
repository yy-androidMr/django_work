import os

D_WEBP_PATH = r'F:\django_work\pyHelper\Plugins\webp\bin\dwebp.exe'
SRC = r'F:\django_work\MrYangServer\media_source\pic\draft3'


def webp2pic():
    for root, dirs, files in os.walk(SRC):
        for file in files:
            if '.webp' in file:
                source_path = os.path.join(root, file).replace('\\', '/')
                os.system(D_WEBP_PATH + ' ' + source_path + ' -o ' + source_path + '.png')
                os.remove(source_path)


if __name__ == '__main__':
    webp2pic()
