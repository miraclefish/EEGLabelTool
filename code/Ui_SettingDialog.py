# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\yyy96\Documents\QtProjects\QtApplication\EEGLabelTool\SettingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(267, 151)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout.setObjectName("formLayout")
        self.Label_1 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Label_1.sizePolicy().hasHeightForWidth())
        self.Label_1.setSizePolicy(sizePolicy)
        self.Label_1.setObjectName("Label_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_1)
        self.LineEdit = QtWidgets.QLineEdit(Dialog)
        self.LineEdit.setObjectName("LineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LineEdit)
        self.Label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Label_2.sizePolicy().hasHeightForWidth())
        self.Label_2.setSizePolicy(sizePolicy)
        self.Label_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.ComboBox = QtWidgets.QComboBox(Dialog)
        self.ComboBox.setObjectName("ComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ComboBox)
        self.Label_3 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.Label_3.sizePolicy().hasHeightForWidth())
        self.Label_3.setSizePolicy(sizePolicy)
        self.Label_3.setObjectName("Label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_3)
        self.Widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Widget.sizePolicy().hasHeightForWidth())
        self.Widget.setSizePolicy(sizePolicy)
        self.Widget.setObjectName("Widget")
        self.colorWidget = QtWidgets.QWidget(self.Widget)
        self.colorWidget.setGeometry(QtCore.QRect(0, 0, 111, 30))
        self.colorWidget.setObjectName("colorWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.colorWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.colorWidget)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.colorWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Widget)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Label_1.setText(_translate("Dialog", "标签名称"))
        self.Label_2.setText(_translate("Dialog", "标签类型"))
        self.Label_3.setText(_translate("Dialog", "标签颜色"))
