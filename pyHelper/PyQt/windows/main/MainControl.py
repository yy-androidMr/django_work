from pprint import pprint

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QFileDialog

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
            self.source_dir.setText(directory1)
