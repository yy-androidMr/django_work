import os

import shutil

if __name__ == '__main__':
    desc = r'G:\pyWorkspace\django_work\MrYangServer\static\projects\gallery\firstLevel\css'
    if os.path.exists(desc):
        shutil.rmtree(desc)
        # os.removedirs(desc)
