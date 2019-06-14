import os
import subprocess
from pathlib import Path


def is_movie(path):
    if not any(str_ in str(path).lower() for str_ in
               ('.mp4', '.mkv', '.rmvb', '.avi', '.rm', '.mov', '.wmv', '.flv', '.aac', '.ogg', '.rm'
                )):
        return False
    return True


def process_cmd(cmd, call=None, done_call=None, param=None):
    ps = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    cmd_str = []
    while True:
        data = ps.stdout.readline()
        if data == b'':
            if ps.poll() is not None:
                if done_call is not None:
                    done_call(cmd_str, param)
                break
        else:
            line = data.decode('utf-8')
            # print(line, end='')
            cmd_str.append(line.replace('\r\n', ''))
            if call is not None:
                call(line)


ffmpeg = input('输入ffmpeg文件路径:\n')
convert_dir = input('输入要转换文件夹的路径:\n')
for root, dirs, files in os.walk(convert_dir):
    for file in files:
        src = os.path.join(root, file)
        if not is_movie(src):
            continue
        Path(src)
        desc = Path(src).with_suffix('.mp4')
        convert_middle = Path(src).with_suffix('.txt')
        if convert_middle.exists():
            if desc.exists():
                os.remove(str(desc))
        if desc.exists():
            continue
        else:
            with open(str(convert_middle), 'w'):
                pass
        cmd_str = ffmpeg + ' -i \"' + src + '\" \"' + str(desc) + '\"'
        print(cmd_str)
        process_cmd(cmd_str)
        os.remove(str(convert_middle))
        # process_cmd(cmd_str)
        # with open()
        # print(cmd_str)
