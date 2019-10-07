import nonebot as nonebot
from qqbot import RunBot, qqbotslot


@qqbotslot
def onQQMessage(bot, contact, member, content):
    if content == '笑话':
        bot.SendTo(contact, "笑话哈哈哈")
    elif content == '-stop':
        bot.SendTo(contact, '机器人已关闭')
        bot.Stop()


def start():
    nonebot.init()
    nonebot.load_builtin_plugins()
    nonebot.run(host='127.0.0.1',port=8080)

start()