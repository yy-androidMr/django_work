from PyQt5.QtWidgets import QMessageBox


class MBox():
    def i(self,w, content):
        QMessageBox.information(w, "提示", content)
        # print(button)
        #
        # msg = QMessageBox()
        # msg.setWindowTitle('提示')
        # msg.setText(content)
        # msg.addButton('确定')
        # res = msg.exec()
        # print(res)
