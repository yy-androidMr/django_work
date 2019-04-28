import os

from utils.ThreadingPool import ThreadingPool as tp
from MediaService import MediaService as ms
from PicService import PicService as ps

if __name__ == '__main__':
    os.symlink(r'E:\DGM\yangyu_SKY-20190415GHW_1187\x5_mobile\mobile_dancer\trunk\mac', './link_da')
    # file = open(r'D:\python\django_work\MryangService\frames\link_da\chmod.command', 'r')
    # print(file.readlines())
    # tp = tp()
    # tp.append(ms().start)
    # tp.append(ps().start)
    # tp.start()
