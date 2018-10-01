import os
import pickle
import shutil

from frames import yutils

cd_count = '../' * 4

source_root = ''.join([cd_count, yutils.media_source, '/movie/src'])
target_root = ''.join([cd_count, yutils.media_source, '/movie/desc'])
net_static_root = yutils.transform_path(cd_count, yutils.static_media_root, '/movie')
net_ts_root = yutils.transform_path(cd_count, yutils.static_media_root, '/movie_ts')


def create_ffmpeg_bat():
    bat_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if not yutils.is_movie(file):
                continue
            (_, source_abs_path, target_abs_path, _) = yutils.decompose_path(
                root, file, source_root, target_root, exten='.mp4')
            peg = os.path.abspath('output/exe/ffmpeg')
            if os.path.exists(target_abs_path):
                continue
            yutils.create_dirs(target_abs_path)
            if '.mp4' in file:
                shutil.copy(source_abs_path, target_abs_path)
                continue
            # '%s -i %s -d 900 %s'

            bat_list.append('%s -i %s %s' % (peg, source_abs_path, target_abs_path))

    return bat_list


# 生成ffmpeg的bat文件,提供批量转换.
def create_convert_bats():
    bat_list = create_ffmpeg_bat()
    dir = "output/"
    yutils.create_dirs(dir)

    for root, dirs, files in os.walk(source_root):
        for file in files:
            if '.bat' in file:
                os.remove(file)
    # shutil.del
    index = 0
    for bat_line in bat_list:
        # mystr = os.popen("bat_line")
        # break
        file_ = ''.join([dir, str(index), '.sh' if yutils.is_mac() else '.bat'])
        index += 1
        with open(file_, 'w+') as f:
            f.write(bat_line)


# 第二需求: 视频切片
def create_ts(root, file, last_path):
    (_, _, _, target_rela_path_ts) = yutils.decompose_path(root, file, target_root, net_ts_root)
    ts_dir = os.path.dirname(target_rela_path_ts) + last_path

    return ts_dir


def cut_call(str):
    pass


def cut_end():
    print('end')


def cut_video():
    # 假设已经读取了
    for root, dirs, files in os.walk(target_root):
        for file in files:
            if '.mp4' in file.lower():
                (_, source_abs_path, target_abs_path, target_rela_path) = yutils.decompose_path(root, file,
                                                                                                target_root,
                                                                                                net_static_root)
                # source_rela_path = os.path.join(root, file)
                last_path = '/' + yutils.md5_of_str(os.path.basename(target_abs_path)) + yutils.M3U8_DIR_EXTEN
                target_dir = os.path.dirname(target_rela_path) + last_path

                ts_dir = create_ts(root, file, last_path)
                print(target_dir)
                # if os.path.exists(target_dir):
                if False:
                    # 不做处理.重复切片
                    print('cut exists %s %s' % (source_abs_path, target_dir))
                    pass
                else:
                    yutils.create_dirs(target_dir, True)
                    yutils.create_dirs(ts_dir, True, True)
                    info = {}  # map形式存储
                    info[yutils.MOVIE_INFO_NAME] = yutils.file_name(os.path.basename(file))
                    with open(''.join([target_dir, '/info']), 'wb') as f:
                        pickle.dump(info, f)  # 只能以二进制写入

                    peg = os.path.abspath('output/exe/ffmpeg')

                    cmd = peg + ' -i ' + source_abs_path + ' -codec copy -vbsf h264_mp4toannexb -map 0 -f segment -segment_list ' + target_dir + '/' + yutils.M3U8_NAME + ' -segment_time 5 ' + ts_dir + '/%03d.ts'
                    print(cmd)
                    yutils.process_cmd(cmd, done_call=cut_end)
                    print('done:' + target_dir)


if __name__ == '__main__':
    # pass
    cut_video()
    # create_convert_bats()

    # mystr = os.popen("ping www.baidu.com")  # popen与system可以执行指令,popen可以接受返回对象
    # mystr = mystr.read()  # 读取输出
    #
    # print("hello", mystr)

    # sub = os.popen("ping www.baidu.com", shell=True, stdout=subprocess.PIPE)
    # sub.wait()
    # print(sub.read())
