# coding:utf-8
# 一些常数设定.

from frames import TmpUtil

DEVELOPMENT_TYPE_KEY = 'DEVELOPMENT_TYPE_KEY'
CUT_MEDIA = False

HOME_MINI = 1
HOME_PC = 2
MAC = 3
COMPANY_PC = 4
T_SERVER = 5
SURFACE_6 = 6

# mediaservice 转码时,是否判断desc中文件存在要不要覆盖.  True为覆盖.
MEDIA_SERVICE_COVER_DESC = False

# true代表使用本地数据库. 
USE_LOCAL_DB = True
TEST_MEIDA_DIR_TAGS = True  # 自动填充 media的tags

development_type = {
    HOME_MINI: '家里mini机',
    HOME_PC: '家里pc机',
    MAC: 'MAC',
    COMPANY_PC: '公司',
    T_SERVER: '腾讯云',
    SURFACE_6: 'surface6',
}


def dev_space():
    development_id = TmpUtil.get(DEVELOPMENT_TYPE_KEY, -1)
    return development_id


def run_init():
    development_id = TmpUtil.get(DEVELOPMENT_TYPE_KEY, -1)
    while development_id not in development_type:
        development_id = int(input('请指定开发场景%s:\n' % str(development_type)))
    TmpUtil.set(DEVELOPMENT_TYPE_KEY, development_id, False)
    if development_id == HOME_MINI:
        global USE_LOCAL_DB
        USE_LOCAL_DB = False
    # if development_id != T_SERVER:
    #     TmpUtil.check_tmp_paths()


run_init()
