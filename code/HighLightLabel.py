from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPalette, QColor

class HighLightLabel(QLabel):
    clicked = pyqtSignal(str, bool)

    highlight = False

    def mousePressEvent(self, ev):
        currentColor = self.palette().windowText().color().name()
        re = QPalette()
        re.setColor(QPalette.WindowText, Qt.yellow)
        re.setColor(QPalette.Window, Qt.black)
        bl = QPalette()
        bl.setColor(QPalette.WindowText, Qt.black)
        bl.setColor(QPalette.Window, QColor("#f0f0f0"))
        if currentColor == "#000000":
            self.setPalette(re)
            self.highlight = True
        elif currentColor == "#ffff00":
            self.setPalette(bl)
            self.highlight = False

        self.clicked.emit(self.objectName(), self.highlight)