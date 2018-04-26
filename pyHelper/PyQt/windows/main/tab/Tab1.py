import datetime
import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from PyQt.Frame.DataSave import DataSave
from PyQt.Ids import HTImport
import shutil


class Tab1():
    def replace(self, lines, pre_str):
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

    def replace_content(self, path, pre_str):
        fp = open(path, 'r+', encoding='utf-8')  # 打开你要写得文件test2.txt
        lines = fp.readlines()  # 打开文件，读入每一行
        self.replace(lines, pre_str)
        fp.seek(0)
        fp.writelines(lines)
        fp.close()  # 关闭文件

    def organize_html(self, src_dir, pre_str):
        filter_type = '.html'
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(filter_type):
                    self.insert_log(file)
                    self.replace_content(os.path.join(root, file), r'/static/projects%s/' % pre_str)
        self.insert_log('convert over')

    def insert_log(self, log_content):
        print(log_content)
        # 4 / 25 / 2018  5: 05:26
        self.log_ctrl.append('[%s]:%s' % (datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'), str(log_content)))

    def handle_click(self, main_c, sender_id):
        self.log_ctrl = main_c.action_log

        if sender_id == HTImport.exc:
            t_dir = main_c.template_dir.text()
            w_n = main_c.web_name.text()
            self.organize_html(t_dir, w_n)
            source = main_c.source_dir.text()
            if not source:  # 空的话
                pass
            else:
                for (root, dirs, files) in os.walk(source):
                    has_cj = main_c.has_css_js(dirs)
                    if has_cj:
                        s_d = main_c.static_dir.text()
                        for s_s in ['css', 'img', 'js', 'sass', 'fonts']:
                            path = os.path.join(root, s_s)
                            if os.path.exists(path):
                                desc = s_d + '/projects' + w_n + '/' + s_s
                                if os.path.exists(desc):
                                    shutil.rmtree(desc)
                                    self.insert_log('desc exist,delete suc!')
                                shutil.copytree(path, desc)
                                self.insert_log('copy success')
                        break
        elif sender_id == HTImport.save:
            save_info = []
            str = main_c.source_dir.text()
            if str:
                save_info.append(str)
            else:
                save_info.append('')
            str = main_c.template_dir.text()
            if str:
                save_info.append(str)
            else:
                save_info.append('')
            str = main_c.static_dir.text()
            if str:
                save_info.append(str)
            else:
                save_info.append('')
            str = main_c.web_name.text()
            if str:
                save_info.append(str)
            else:
                save_info.append('')
            DataSave.save('templatePath', save_info)
        elif sender_id == HTImport.load:
            save_info = DataSave.read('templatePath')
            self.insert_log(save_info)
            if len(save_info) <= 0:
                return
            main_c.source_dir.setText(save_info[0])
            main_c.template_dir.setText(save_info[1])
            main_c.static_dir.setText(save_info[2])
            main_c.web_name.setText(save_info[3])
            # save_info.append(str)
            # DataSave.save('templatePath', str)
        else:
            select_dir = QFileDialog.getExistingDirectory(main_c, "选取文件夹", "./")  # 起始路径
            if not select_dir:
                self.insert_log('select cancel')
                return
            if sender_id == HTImport.s_btn:  # 源文件按钮id
                has_cj = False
                for (root, dirs, files) in os.walk(select_dir):
                    has_cj = main_c.has_css_js(dirs)
                    if has_cj:
                        main_c.source_dir.setText(select_dir)
                        break

                if not has_cj:
                    QMessageBox.information(main_c, "提示", '源文件格式错误')
            elif sender_id == HTImport.t_btn:  # template 按钮id
                t_str = 'templates'
                if t_str in select_dir:
                    main_c.template_dir.setText(select_dir)
                    web_name = select_dir[select_dir.rfind(t_str) + len(t_str):]
                    main_c.web_name.setText(web_name)
                else:
                    QMessageBox.information(main_c, "提示", '模板文件路径错误')
            elif sender_id == HTImport.static_btn:  # static 按钮id
                if select_dir.endswith('static'):
                    main_c.static_dir.setText(select_dir)
                else:
                    QMessageBox.information(main_c, "提示", '请指向到static根目录')

                    # print(button)

                    # button = QMessageBox.question(self, "Question", "检测到程序有更新，是否安装最新版本？",
                    #                               QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
                    # MBox.i(MainControl,directory1)
                    # self.source_dir.setText(directory1)
