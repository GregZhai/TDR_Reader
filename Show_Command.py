# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Show_Command.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Show_Command(object):
    def setupUi(self, Show_Command):
        Show_Command.setObjectName("Show_Command")
        Show_Command.resize(1362, 889)
        self.centralwidget = QtWidgets.QWidget(Show_Command)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit_command = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_command.setGeometry(QtCore.QRect(40, 30, 1301, 61))
        self.textEdit_command.setObjectName("textEdit_command")
        self.pushButton_SendCommand = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SendCommand.setGeometry(QtCore.QRect(290, 110, 131, 31))
        self.pushButton_SendCommand.setObjectName("pushButton_SendCommand")
        self.pushButton_Close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Close.setGeometry(QtCore.QRect(1070, 110, 141, 31))
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.textEdit_SSHoutput = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_SSHoutput.setGeometry(QtCore.QRect(40, 160, 1301, 691))
        self.textEdit_SSHoutput.setObjectName("textEdit_SSHoutput")
        self.label_will_sent_to = QtWidgets.QLabel(self.centralwidget)
        self.label_will_sent_to.setGeometry(QtCore.QRect(50, 10, 131, 16))
        self.label_will_sent_to.setObjectName("label_will_sent_to")
        self.label_server = QtWidgets.QLabel(self.centralwidget)
        self.label_server.setGeometry(QtCore.QRect(180, 10, 121, 16))
        self.label_server.setText("")
        self.label_server.setObjectName("label_server")
        self.label_command_view = QtWidgets.QLabel(self.centralwidget)
        self.label_command_view.setGeometry(QtCore.QRect(320, 10, 131, 16))
        self.label_command_view.setObjectName("label_command_view")
        self.pushButton_ClearOutput = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ClearOutput.setGeometry(QtCore.QRect(880, 110, 131, 31))
        self.pushButton_ClearOutput.setObjectName("pushButton_ClearOutput")
        self.label_caution = QtWidgets.QLabel(self.centralwidget)
        self.label_caution.setGeometry(QtCore.QRect(20, 100, 261, 16))
        self.label_caution.setText("")
        self.label_caution.setObjectName("label_caution")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(60, 120, 171, 20))
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")
        self.pushButton_CopyOutput = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_CopyOutput.setGeometry(QtCore.QRect(670, 110, 151, 31))
        self.pushButton_CopyOutput.setObjectName("pushButton_CopyOutput")
        self.pushButton_StopCommand = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_StopCommand.setGeometry(QtCore.QRect(480, 110, 131, 31))
        self.pushButton_StopCommand.setObjectName("pushButton_StopCommand")
        Show_Command.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Show_Command)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1362, 21))
        self.menubar.setObjectName("menubar")
        Show_Command.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Show_Command)
        self.statusbar.setObjectName("statusbar")
        Show_Command.setStatusBar(self.statusbar)

        self.retranslateUi(Show_Command)
        QtCore.QMetaObject.connectSlotsByName(Show_Command)

    def retranslateUi(self, Show_Command):
        _translate = QtCore.QCoreApplication.translate
        Show_Command.setWindowTitle(_translate("Show_Command", "Single Server"))
        self.pushButton_SendCommand.setText(_translate("Show_Command", "Send Command"))
        self.pushButton_Close.setText(_translate("Show_Command", "Close Window"))
        self.label_will_sent_to.setText(_translate("Show_Command", "Command will be sent to : "))
        self.label_command_view.setText(_translate("Show_Command", "Command as following:"))
        self.pushButton_ClearOutput.setText(_translate("Show_Command", "Clear Output"))
        self.pushButton_CopyOutput.setText(_translate("Show_Command", "Copy All"))
        self.pushButton_StopCommand.setText(_translate("Show_Command", "Stop Command"))

