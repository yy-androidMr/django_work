import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from untitled import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)
window = Ui_MainWindow()
mainWindow = QMainWindow()
window.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())