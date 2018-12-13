# coding:utf-8

import logging

import sys

import time

from frames import TmpUtil


def logname():
    return time.strftime('%Y-%m-%d %H_%M_%S', time.localtime()) + '.log'


logging.basicConfig(level=logging.INFO,
                    filename=TmpUtil.log_path(logname()),
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
