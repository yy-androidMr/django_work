import sys
from PyQt5.QtWidgets import QApplication

from PyQt.windows.main.MainControl import MainControl
from PyQt.windows.main.tab.Tab1 import Tab1

if __name__=='__main__':
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainControl()
    main_window.show()
<<<<<<< HEAD
    sys.exit(app.exec_())    sys.exit(app.exec_())
=======
>>>>>>> 1a5cfb28d17c7bb9d7f89d41420343b43557f571
    sys.exit(app.exec_())
