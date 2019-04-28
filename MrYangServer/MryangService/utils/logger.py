# coding:utf-8

import logging

import sys

import time

from frames import TmpUtil


def logname():
    return time.strftime('%Y-%m-%d %H_%M_%S', time.localtime()) + '.log'


logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(TmpUtil.log_path(logname()))
console_handler = logging.StreamHandler()
file_formatter = logging.Formatter(
    '[%(asctime)s][%(filename)s:%(lineno)d]%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
# console_formatter = logging.Formatter(
#     '[%(asctime)s][%(filename)s:%(lineno)d]%(levelname)s: %(message)s')
console_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def error(*args):
    log(logging.ERROR, *args)


def warn(*args):
    log(logging.WARN, *args)


def debug(*args):
    log(logging.DEBUG, *args)


def info(*args):
    log(logging.INFO, *args)
    # logger.info(''.join(args))


def log(level, *args):
    logger.log(level, ' '.join(args))

# logging.basicConfig(level=logging.INFO,
#                     filename=TmpUtil.log_path(logname()),
#                     filemode='a',
#                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
