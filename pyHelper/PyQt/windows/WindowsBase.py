from PyQt5.QtWidgets import QMainWindow


class WindowsBase(QMainWindow):
    def __init__(self, parent=None):
        super(WindowsBase, self).__init__(parent)

    def sender_id(self):
        sender = self.sender()
        try:
            id = sender.property('id')
            return id
        except:
            print('sender is not id property %s' % sender.objectName())
            pass
        return -1