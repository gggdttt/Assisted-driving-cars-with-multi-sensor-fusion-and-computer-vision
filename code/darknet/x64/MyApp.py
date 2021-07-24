# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyApp.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(555, 490)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setBaseSize(QtCore.QSize(550, 640))
        self.showLogView = QtWidgets.QTextBrowser(Form)
        self.showLogView.setGeometry(QtCore.QRect(20, 60, 491, 101))
        self.showLogView.setObjectName("showLogView")
        self.buttonConnect = QtWidgets.QPushButton(Form)
        self.buttonConnect.setEnabled(False)
        self.buttonConnect.setGeometry(QtCore.QRect(20, 220, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonConnect.sizePolicy().hasHeightForWidth())
        self.buttonConnect.setSizePolicy(sizePolicy)
        self.buttonConnect.setObjectName("buttonConnect")
        self.buttonDown = QtWidgets.QPushButton(Form)
        self.buttonDown.setGeometry(QtCore.QRect(190, 350, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonDown.sizePolicy().hasHeightForWidth())
        self.buttonDown.setSizePolicy(sizePolicy)
        self.buttonDown.setObjectName("buttonDown")
        self.buttonEmergencyStop = QtWidgets.QPushButton(Form)
        self.buttonEmergencyStop.setGeometry(QtCore.QRect(360, 220, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonEmergencyStop.sizePolicy().hasHeightForWidth())
        self.buttonEmergencyStop.setSizePolicy(sizePolicy)
        self.buttonEmergencyStop.setObjectName("buttonEmergencyStop")
        self.buttonRight = QtWidgets.QPushButton(Form)
        self.buttonRight.setGeometry(QtCore.QRect(360, 350, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRight.sizePolicy().hasHeightForWidth())
        self.buttonRight.setSizePolicy(sizePolicy)
        self.buttonRight.setObjectName("buttonRight")
        self.buttonLeft = QtWidgets.QPushButton(Form)
        self.buttonLeft.setGeometry(QtCore.QRect(20, 350, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonLeft.sizePolicy().hasHeightForWidth())
        self.buttonLeft.setSizePolicy(sizePolicy)
        self.buttonLeft.setObjectName("buttonLeft")
        self.buttonUp = QtWidgets.QPushButton(Form)
        self.buttonUp.setGeometry(QtCore.QRect(190, 220, 161, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonUp.sizePolicy().hasHeightForWidth())
        self.buttonUp.setSizePolicy(sizePolicy)
        self.buttonUp.setObjectName("buttonUp")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 40, 72, 15))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.showLogView.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt;\">Stop</span></p></body></html>"))
        self.buttonConnect.setText(_translate("Form", "连接"))
        self.buttonDown.setText(_translate("Form", "↓"))
        self.buttonEmergencyStop.setText(_translate("Form", "急停"))
        self.buttonRight.setText(_translate("Form", "→"))
        self.buttonLeft.setText(_translate("Form", "←"))
        self.buttonUp.setText(_translate("Form", "↑"))
        self.label.setText(_translate("Form", "运行状态"))
