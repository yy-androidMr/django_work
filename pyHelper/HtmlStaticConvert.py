# 转换模板中, 网页的css调用.
# 比如templates/own_index/ 所有的css,js,img 引用,转换到/static/projects/own_index
# 需求: 两个相对或者绝对路径. 搜索替换.替换规则写死
import os


def replace(lines, pre_str):
    regex = [(r'<script src="js', r'<script src="' + pre_str + 'js'),
                  (r'<img src="img', r'<img src="' + pre_str + 'img'),
                  (r'href="css', r'href="' + pre_str + 'css'),
                  (r'href="img', r'href="' + pre_str + 'img')]
    index = 0
    for line in lines:
        new_line = line
        for src, desc in regex:
            new_line = new_line.replace(src, desc)
            lines[index] = new_line
        index += 1


def replace_content(path, pre_str):
    fp = open(path, 'r+', encoding='utf-8')  # 打开你要写得文件test2.txt
    lines = fp.readlines()  # 打开文件，读入每一行
    replace(lines, pre_str)
    fp.seek(0)
    fp.writelines(lines)
    fp.close()  # 关闭文件


if __name__ == '__main__':
    print('convert begin')
    src_dir = r'G:\pyWorkspace\django_work\MrYangServer\templates\own_index'
    static_replace = r'G:\pyWorkspace\django_work\MrYangServer\static\projects\own_index'

    filter_type = '.html'
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(filter_type):
                print(file)
                replace_content(os.path.join(root, file), r'/static/projects/own_index/')
    print('onvert over')
