# coding:utf-8
# 一些常数设定.

from  frames import ypath, TmpUtil, logger

DEVELOPMENT_TYPE_KEY = 'DEVELOPMENT_TYPE_KEY'

HOME_MINI = 1
HOME_PC = 2
MAC = 3
COMPANY_PC = 4
T_SERVER = 5

development_type = {
    HOME_MINI: '家里mini机',
    HOME_PC: '家里pc机',
    MAC: 'MAC',
    COMPANY_PC: '公司',
    T_SERVER: '腾讯云',
}


def dev_space():
    development_id = TmpUtil.get(DEVELOPMENT_TYPE_KEY, -1)
    return development_id


def run_init():
    development_id = TmpUtil.get(DEVELOPMENT_TYPE_KEY, -1)
    while development_id not in development_type:
        development_id = int(input('请指定开发场景%s:\n' % str(development_type)))
    TmpUtil.set(DEVELOPMENT_TYPE_KEY, development_id, False)
    # if development_id != T_SERVER:
    #     TmpUtil.check_tmp_paths()


run_init()
