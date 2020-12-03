from Ui_SavingDialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

class SavingDialog(QDialog):

    def __init__(self, filename, age, gender,l, text, num, types):
        super(SavingDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("预览将要保存的信息")
        self.setWindowModality(Qt.ApplicationModal)

        
        self.ui.Filename.setText(filename)
        self.ui.Age.setText("{}岁{}个月".format(age[0], age[1]))
        self.ui.Gender.setText(gender)
        self.ui.textEdit.setText(text)
        self.ui.length.setText("{}s".format(l))
        self.ui.Num.setText("{}个已标注的片段".format(num))
        self.ui.types.setText(str(types))