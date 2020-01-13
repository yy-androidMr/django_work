# import pygame  # pip install pygame
#
# def playMusic(filename, loops=0, start=0.0, value=0.5):
#     """
#     :param filename: 文件名
#     :param loops: 循环次数
#     :param start: 从多少秒开始播放
#     :param value: 设置播放的音量，音量value的范围为0.0到1.0
#     :return:
#     """
#     flag = False  # 是否播放过
#     pygame.mixer.init()  # 音乐模块初始化
#     while 1:
#         if flag == 0:
#             pygame.mixer.music.load(filename)
#             # pygame.mixer.music.play(loops=0, start=0.0) loops和start分别代表重复的次数和开始播放的位置。
#             pygame.mixer.music.play(loops=loops, start=start)
#             pygame.mixer.music.set_volume(value)  # 来设置播放的音量，音量value的范围为0.0到1.0。
#         if pygame.mixer.music.get_busy() == True:
#             flag = True
#         else:
#             if flag:
#                 pygame.mixer.music.stop()  # 停止播放
#                 break
#
# if __name__ == "__main__":
#     playMusic('build_finish.mp3')
# import winsound
#
# winsound.PlaySound(
#     r"E:\DGM\yangyu_SKY-20190415GHW_1187\x5_mobile\mr\Resources\音效资源\ui_sound_effect\pet_rc_hailuo_s.mp3",
#     winsound.SND_ASYNC)
#
import time

import pygame
pygame.mixer.init()
print(u"播放音乐1")
track = pygame.mixer.music.load(r"sound")
pygame.mixer.music.play()
while True:
    time.sleep(0.3)
    if(pygame.mixer.music.get_busy()!=1):
        break
print('结束')
#pygame.mixer.music.pause() #暂停
#pygame.mixer.music.unpause()#取消暂停
#成功播放音乐，并有暂停，取消暂停功能。