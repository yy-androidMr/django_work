# coding:utf-8


def enum(**enums):
    return type('Enum', (), enums)


# 通用成功
SUC = '成功'

# 登录错误枚举
LOGIN = enum(SUC='成功', NO_ACCOUNT='帐号或密码错误', OTHER='其他错误')
UPLOAD = enum(NO_LOGIN='您没有登录')
REGIST =enum(OTHER='其他错误')
# print LOGIN.NO_ACCOUNT
