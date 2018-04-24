from pprint import pprint

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

    def select_dir(self):
        if super().sender_id() == HTImport.s_btn:
            directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
            # button = QMessageBox.question(self, "Question", "检测到程序有更新，是否安装最新版本？",
            #                               QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            MBox.i(MainControl,directory1)
            # self.source_dir.setText(directory1)
