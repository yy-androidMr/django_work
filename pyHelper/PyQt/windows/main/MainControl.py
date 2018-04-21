from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow

from PyQt.windows.main.MainWindow import Ui_MainWindow


class MainControl(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainControl, self).__init__(parent)
        self.setupUi(self)
        # self.action_exit.triggered.connect(self.onExitTriggered)
        #
        # self.action_copy.triggered.connect(self.onCopyTriggered)
        # self.action_paste.triggered.connect(self.onPasteTriggered)
        # self.action_cut.triggered.connect(self.onCutTriggered)

    def main_btn_click(self):
        QtWidgets.QMessageBox.information(self.pushButton, "标题", "这是第一个PyQt5 GUI程序")
