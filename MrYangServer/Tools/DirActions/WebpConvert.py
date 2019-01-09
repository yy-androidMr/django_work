import os

D_WEBP_PATH = r'G:\github\files\webp\libwebp-1.0.0-windows-x64\bin\dwebp.exe'
SRC = r'G:\cache\work_cache\draft'


def webp2pic():
    for root, dirs, files in os.walk(SRC):
        for file in files:
            if '.webp' in file:
                source_path = os.path.join(root, file).replace('\\', '/')
                os.system(D_WEBP_PATH + ' ' + source_path + ' -o ' + source_path + '.png')
                os.remove(source_path)


if __name__ == '__main__':
    webp2pic()
