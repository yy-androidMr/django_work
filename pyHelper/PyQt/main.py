import sys
from PyQt5.QtWidgets import QApplication

from PyQt.windows.main.MainControl import MainControl
from PyQt.windows.main.tab.Tab1 import Tab1

if __name__=='__main__':
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainControl()
    main_window.show()
    sys.exit(app.exec_())    sys.exit(app.exec_())
