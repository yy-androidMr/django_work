from pprint import pprint

import os

import shutil
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from PyQt.Frame.MBox import MBox
from PyQt.Ids import HTImport
from PyQt.windows.WindowsBase import WindowsBase
from PyQt.windows.main.MainWindow import Ui_MainWindow


class MainControl(WindowsBase, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainControl, self).__init__(parent)
        self.setupUi(self)
        # self.action_exit.triggered.connect(self.onExitTriggered)
        #
        # self.action_copy.triggered.connect(self.onCopyTriggered)
        # self.action_paste.triggered.connect(self.onPasteTriggered)
        # self.action_cut.triggered.connect(self.onCutTriggered)

    def has_css_js(self, dirs):
        if 'css' in dirs:
            if 'js' in dirs:
                return True
        return False

    # def organgization_cj(self):

    def select_dir(self):
        if super().sender_id() == HTImport.exc:
            t_dir = self.template_dir.text()
            w_n = self.web_name.text()

            source = self.source_dir.text()
            if not source:  # 空的话
                pass
            else:
                for (root, dirs, files) in os.walk(source):
                    has_cj = self.has_css_js(dirs)
                    if has_cj:
                        s_d = self.static_dir.text()
                        for s_s in ['css', 'img', 'js', 'sass']:
                            path = os.path.join(root, s_s)
                            if os.path.exists(path):
                                desc = s_d + '/projects' + w_n + '/' + s_s
                                print('from:' + path, 'to:' + desc)
                                shutil.copytree(path, desc)
                        break
        else:
            select_dir = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
            if super().sender_id() == HTImport.s_btn:  # 源文件按钮id
                has_cj = False
                for (root, dirs, files) in os.walk(select_dir):
                    has_cj = self.has_css_js(dirs)
                    if has_cj:
                        self.source_dir.setText(select_dir)
                        # self.source_paths = []
                        # for s_s in ['css', 'img', 'js', 'sass']:
                        #     path = os.path.join(root, s_s)
                        #     if os.path.exists(path):
                        #         self.source_paths.append(path)
                        break

                if not has_cj:
                    QMessageBox.information(self, "提示", '源文件格式错误')
            elif super().sender_id() == HTImport.t_btn:  # template 按钮id
                t_str = 'templates'
                if t_str in select_dir:
                    self.template_dir.setText(select_dir)
                    web_name = select_dir[select_dir.rfind(t_str) + len(t_str):]
                    self.web_name.setText(web_name)
                else:
                    QMessageBox.information(self, "提示", '模板文件路径错误')
            elif super().sender_id() == HTImport.static_btn:  # static 按钮id
                if select_dir.endswith('static'):
                    self.static_dir.setText(select_dir)
                else:
                    QMessageBox.information(self, "提示", '请指向到static根目录')

                    # print(button)

                    # button = QMessageBox.question(self, "Question", "检测到程序有更新，是否安装最新版本？",
                    #                               QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
                    # MBox.i(MainControl,directory1)
                    # self.source_dir.setText(directory1)
