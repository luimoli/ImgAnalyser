# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Code_now\ViAnalyser\visecond_single.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowSecondSingle(object):
    def setupUi(self, MainWindowSecondSingle):
        MainWindowSecondSingle.setObjectName("MainWindowSecondSingle")
        MainWindowSecondSingle.resize(891, 639)
        self.centralwidget = QtWidgets.QWidget(MainWindowSecondSingle)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 867, 529))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_map = QtWidgets.QLabel()
        self.label_map.setGeometry(QtCore.QRect(0, 0, 871, 531))
        self.label_map.setObjectName("label_map")
        self.scrollArea.setWidget(self.label_map)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 1, 0, 1, 1)
        MainWindowSecondSingle.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowSecondSingle)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 891, 26))
        self.menubar.setObjectName("menubar")
        MainWindowSecondSingle.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowSecondSingle)
        self.statusbar.setObjectName("statusbar")
        MainWindowSecondSingle.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowSecondSingle)
        QtCore.QMetaObject.connectSlotsByName(MainWindowSecondSingle)

    def retranslateUi(self, MainWindowSecondSingle):
        _translate = QtCore.QCoreApplication.translate
        MainWindowSecondSingle.setWindowTitle(_translate("MainWindowSecondSingle", "Figure"))
        self.label_map.setText(_translate("MainWindowSecondSingle", "TextLabel"))
        self.btn_save.setText(_translate("MainWindowSecondSingle", "Save"))
