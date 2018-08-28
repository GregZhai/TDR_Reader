# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Show_Result.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Show_Result(object):
    def setupUi(self, Show_Result):
        Show_Result.setObjectName("Show_Result")
        Show_Result.resize(1301, 982)
        self.centralwidget = QtWidgets.QWidget(Show_Result)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit_Server1 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server1.setGeometry(QtCore.QRect(9, 138, 636, 164))
        self.textEdit_Server1.setObjectName("textEdit_Server1")
        self.textEdit_Server2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server2.setGeometry(QtCore.QRect(651, 138, 635, 164))
        self.textEdit_Server2.setObjectName("textEdit_Server2")
        self.textEdit_Server3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server3.setGeometry(QtCore.QRect(9, 308, 636, 165))
        self.textEdit_Server3.setObjectName("textEdit_Server3")
        self.textEdit_Server4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server4.setGeometry(QtCore.QRect(651, 308, 635, 165))
        self.textEdit_Server4.setObjectName("textEdit_Server4")
        self.textEdit_Server5 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server5.setGeometry(QtCore.QRect(9, 479, 636, 164))
        self.textEdit_Server5.setObjectName("textEdit_Server5")
        self.textEdit_Server6 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server6.setGeometry(QtCore.QRect(651, 479, 635, 164))
        self.textEdit_Server6.setObjectName("textEdit_Server6")
        self.textEdit_Server7 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server7.setGeometry(QtCore.QRect(9, 649, 636, 165))
        self.textEdit_Server7.setObjectName("textEdit_Server7")
        self.textEdit_Server8 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server8.setGeometry(QtCore.QRect(651, 649, 635, 165))
        self.textEdit_Server8.setObjectName("textEdit_Server8")
        self.textEdit_Server9 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server9.setGeometry(QtCore.QRect(9, 820, 636, 164))
        self.textEdit_Server9.setObjectName("textEdit_Server9")
        self.textEdit_Server10 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Server10.setGeometry(QtCore.QRect(651, 820, 635, 164))
        self.textEdit_Server10.setObjectName("textEdit_Server10")
        self.label_will_sent_to = QtWidgets.QLabel(self.centralwidget)
        self.label_will_sent_to.setGeometry(QtCore.QRect(30, 10, 131, 16))
        self.label_will_sent_to.setObjectName("label_will_sent_to")
        self.label_command_view = QtWidgets.QLabel(self.centralwidget)
        self.label_command_view.setGeometry(QtCore.QRect(300, 10, 131, 16))
        self.label_command_view.setObjectName("label_command_view")
        self.textEdit_command = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_command.setGeometry(QtCore.QRect(20, 40, 1231, 41))
        self.textEdit_command.setObjectName("textEdit_command")
        self.label_server = QtWidgets.QLabel(self.centralwidget)
        self.label_server.setGeometry(QtCore.QRect(170, 10, 101, 16))
        self.label_server.setText("")
        self.label_server.setObjectName("label_server")
        self.pushButton_Close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Close.setGeometry(QtCore.QRect(720, 90, 181, 41))
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.pushButton_SendCommand = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SendCommand.setGeometry(QtCore.QRect(380, 90, 181, 41))
        self.pushButton_SendCommand.setObjectName("pushButton_SendCommand")
        Show_Result.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Show_Result)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1301, 21))
        self.menubar.setObjectName("menubar")
        Show_Result.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Show_Result)
        self.statusbar.setObjectName("statusbar")
        Show_Result.setStatusBar(self.statusbar)

        self.retranslateUi(Show_Result)
        QtCore.QMetaObject.connectSlotsByName(Show_Result)

    def retranslateUi(self, Show_Result):
        _translate = QtCore.QCoreApplication.translate
        Show_Result.setWindowTitle(_translate("Show_Result", "Region Servers"))
        self.textEdit_Server5.setHtml(_translate("Show_Result", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_will_sent_to.setText(_translate("Show_Result", "Command will be sent to : "))
        self.label_command_view.setText(_translate("Show_Result", "Command as following:"))
        self.pushButton_Close.setText(_translate("Show_Result", "Close or Modify Command"))
        self.pushButton_SendCommand.setText(_translate("Show_Result", "Send Command"))

