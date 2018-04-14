# -*- coding: utf-8 -*-
import argparse

from qqbot import QQBotSlot as qqbotslot, RunBot, QQBot

from qq_login import ThreadManager

DOWNLOAD = '-dl'
RUNNINGTHREAD = '-tl'
HELP = '-help'
HELPDIC = {HELP: '帮助', DOWNLOAD: '[\S+]下载某一个链接', RUNNINGTHREAD: '查看正在下载列表'}


@qqbotslot
def onQQMessage(bot, contact, member, content):
    # 过滤掉
    if contact.qq != '1226341090':
        return
        # bot.SendTo(contact, '我不认识你')

    # 开启一个下载
    if content.startswith(DOWNLOAD):
        url = content.replace(DOWNLOAD, '')
        # 'https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi'
        ThreadManager.start_download(url)
        bot.SendTo(contact, url)

    # 查看正在下载的文件
    elif content == RUNNINGTHREAD:
        if ThreadManager.threads and ThreadManager.threads.count() > 0:
            for t in ThreadManager.threads:
                bot.SendTo(contact, '正在下载:%s' % t.getName())
        else:
            bot.SendTo(contact, '没有正在下载的任务!')

    # 帮助命令
    elif content == HELP:
        helplist = ''
        for key, value in HELPDIC.items():
            helplist += key + '  ' + value + '\n'
        bot.SendTo(contact, helplist)

    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='登录qq')
    # parser.add_argument('-q', action='-q 3229213855')
    RunBot(['-q', '3229213855'])
    # bot.Login(['-q','3229213855'])
