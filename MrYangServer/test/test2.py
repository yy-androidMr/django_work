import datetime
import os
from pathlib import Path, PurePath, PureWindowsPath, PosixPath, PurePosixPath

# p = Path('.')
# print([x for x in p.iterdir()])

# pp = PurePath('c:/a//b') / '2'
# ppa = Path('c:/a/b')
#
# ppa.exists()
# print([x for x in pp.parents])
# print(Path('c:/a//b') / 'c')
# print(PureWindowsPath('c:/a/b') / 'd')
#
# print(PurePath('/abc\\2.txt').as_posix())
# print(PurePath('a/b/c').with_name('d.txt'))

#
# print('F:/cache/res/src/media/01-课程介绍.mp4'[len('F:/cache/res/src/media'):])
import psutil

print('cpu数量:' + str(psutil.cpu_count()))
print('cpu 时钟:' + str(psutil.cpu_times()))
print('系统启动时间:' + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

memory = psutil.virtual_memory()
# memory.total
# memory.free
# memory.percent
# memory.used
print(memory.total)

# print('磁盘信息:' + str(psutil.disk_partitions()))
print('磁盘使用情况:' + str(psutil.disk_usage('C:\\')))

print('所有进程:' + str(psutil.pids()))
# print('当前进程id:' + str(os.getpid()))

p = psutil.Process(36556)
print(p.name())
pmem = p.memory_info()
print(pmem)
print('所有线程信息:' + str(p.threads()))
print('我自己的线程信息:' + str(psutil.Process(os.getpid()).threads()))
print('------------结束------------')
