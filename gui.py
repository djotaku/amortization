# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(643, 210)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 611, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditInterest = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditInterest.setObjectName("lineEditInterest")
        self.gridLayout.addWidget(self.lineEditInterest, 0, 3, 1, 1)
        self.lineEditMonth = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditMonth.setObjectName("lineEditMonth")
        self.gridLayout.addWidget(self.lineEditMonth, 0, 5, 1, 1)
        self.pushButtonCalculate = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonCalculate.setObjectName("pushButtonCalculate")
        self.gridLayout.addWidget(self.pushButtonCalculate, 1, 3, 1, 1)
        self.lineEditPrinciple = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditPrinciple.setObjectName("lineEditPrinciple")
        self.gridLayout.addWidget(self.lineEditPrinciple, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEditInterest.setPlaceholderText(_translate("Dialog", "0.0444"))
        self.lineEditMonth.setPlaceholderText(_translate("Dialog", "360"))
        self.pushButtonCalculate.setText(_translate("Dialog", "Calculate"))
        self.lineEditPrinciple.setPlaceholderText(_translate("Dialog", "270000"))
        self.label_2.setText(_translate("Dialog", "Interest"))
        self.label.setText(_translate("Dialog", "Principle"))
        self.label_3.setText(_translate("Dialog", "Number of Months"))


