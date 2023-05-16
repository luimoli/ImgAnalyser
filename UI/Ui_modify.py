# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\vianalyser.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.scrollArea = QtWidgets.QScrollArea(self.horizontalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 997, 657))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.label_img = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_img = QtWidgets.QLabel()
        self.label_img.setGeometry(QtCore.QRect(0, 0, 1001, 661))
        self.label_img.setMouseTracking(True)
        self.label_img.setStyleSheet("")
        self.label_img.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_img.setLineWidth(1)
        self.label_img.setObjectName("label_img")
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.label_img)

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

