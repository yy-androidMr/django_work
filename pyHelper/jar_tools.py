import zipfile
import os


def all_jar_cache(cache_dir=False):
    cache_jar_files = {}
    clz = '.class'
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if not file.endswith('.jar') or 'build\\intermediates' in root:
                continue
            src = os.path.join(root, file)
            zip_file = zipfile.ZipFile(src)
            if cache_dir:
                dirname = []
                for name in zip_file.namelist():
                    dirname.append((os.path.dirname(name)))
                cache_jar_files[src] = set(dirname)
            else:
                cache_jar_files[src] = set(filter(lambda name: name.endswith(clz), zip_file.namelist()))
    return cache_jar_files


def digout_by_jar_path():
    path = None
    while path is None or path is '':
        path = input('输入查找字符:\n')
    path = path.replace('\\', '/')
    search_filter = lambda x: path in x

    cache_jar_files = all_jar_cache()
    for jar_path in cache_jar_files:
        res = list(filter(search_filter, cache_jar_files[jar_path]))
        if len(res) > 0:
            print('查找结果:' + jar_path + '\n' + str(res))
    print('查找结束!')


def jar_intersection():
    cache_jar_files = all_jar_cache()
    cache_new_list = {}
    for jar_path, content in cache_jar_files.items():
        for n_jar_path in cache_new_list:
            intersection = content.intersection(cache_new_list[n_jar_path])
            if len(intersection):
                print('找到重复:\n' + jar_path + '\n' + n_jar_path + '\n重复内容:' + str(intersection))
        cache_new_list[jar_path] = content
    print('重复class查找结束!')


def write_method_count():
    path = None
    lines = {}
    while True:
        while path is None or path is '' or not os.path.isfile(path):
            path = input('输入统计包方法数量的文件路径:\n')
        with open(path, 'r', encoding='utf-8') as f:
            tmp_lines = f.readlines()
            try:
                if len(tmp_lines) > 0:
                    tmp_line_split = tmp_lines[0].split(',')
                    if tmp_line_split[0].isdigit():
                        for line in tmp_lines:
                            split_line = line.strip().split(',')
                            lines[split_line[1].replace('.', '/')] = [split_line[0]]

                        # lines = tmp_lines

                        break
            except:
                pass
    out_list = []
    cache_jar_files = all_jar_cache(True)
    for jar_path, content in cache_jar_files.items():
        # del_list = []
        for pack_key in lines:
            if pack_key in content:
                out_list.append(pack_key)
                out_list.append(lines[pack_key])
                lines[pack_key].append(jar_path)
                # del_list.append(pack_key)
        # for del_item in del_list:
        #     del lines[del_item]

    print(lines)
    print(len(lines))
    with open('D:\cache\method_count\method2.csv', 'w+', encoding='utf-8') as f:
        for line in lines:
            cnt = ''
            for info in lines[line]:
                cnt += str(info) + ','
            f.write(line + ',' + cnt + '\n')
    # 工程中jar包去重


search_dir = ''
while not os.path.isdir(search_dir):
    search_dir = input('输入工程路径:\n')

action_type = None
action_map = {'1': 'jar包去重', '2': '查找对应的class或者路径', '3': '根据统计的方法数量,获取对应的jar包映射'}
while action_type not in action_map:
    cnt = '\n'
    index = 0
    for action in action_map:
        cnt += action + '=' + action_map[action] + '\n'
        index += 1
    action_type = input('输入需要的操作:' + cnt).lower()

action_type = int(action_type)
if (action_type == 1):
    jar_intersection()
elif (action_type == 2):
    digout_by_jar_path()
elif (action_type == 3):
    write_method_count()

# action_list = ['i', 's', 'c']
# action_intro = ['jar包去重', '查找对应的class或者路径']

# while action_type not in action_list:
#     cnt = '\n'
#     index = 0
#     for action in action_list:
#         cnt += action + '=' + action_intro[index] + '\n'
#         index += 1
#     action_type = input('输入需要的操作:' + cnt).lower()
#
# if (action_type == action_list[0]):
#     jar_intersection()
# elif (action_type == action_list[1]):
#     digout_by_jar_path()
# elif (action_type == action_list[2]):
#     write_method_count()
