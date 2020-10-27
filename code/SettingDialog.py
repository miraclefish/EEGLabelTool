from Ui_SettingDialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QColorDialog
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt

class SettingDialog(QDialog):

    def __init__(self):
        super(SettingDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("添加新的标签类型")

        self.NewLabelName = "default"
        self.cbList = ['区间标签','点标签']
        self.LabelType = self.cbList[0]
        self.NewLabelColor = (255,255,255,255)
        self.ui.pushButton.setStyleSheet("QPushButton{background-color:rgb(255,255,255,255)}")

        self.ui.LineEdit.textChanged.connect(lambda:self.changeText(self.ui.LineEdit))
        self.ui.ComboBox.addItems(['区间标签','点标签'])
        self.ui.ComboBox.currentTextChanged.connect(self.changeType)
        self.ui.pushButton.clicked.connect(self.changeColor)

    def changeText(self, text):
        self.NewLabelName = text.text()
    
    def changeType(self, text):
        self.LabelType = text
    
    def changeColor(self):
        color= QColorDialog.getColor()
        style = "QPushButton{background-color:rgb" + str(color.getRgb()) + "}"
        self.ui.pushButton.setStyleSheet(style)
        self.NewLabelColor = color.getRgb()