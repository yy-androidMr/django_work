import traceback

from PyQt.windows.WindowsBase import WindowsBase
from PyQt.windows.main.MainWindow import Ui_MainWindow
from PyQt.windows.main.tab.Tab1 import Tab1


class MainControl(WindowsBase, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainControl, self).__init__(parent)
        self.setupUi(self)

    def has_css_js(self, dirs):
        if 'css' in dirs:
            if 'js' in dirs:
                return True
        return False

    def select_dir(self):
        try:
            Tab1().handle_click(self, super().sender_id())
        except  Exception:
            traceback.print_exc()
