# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Desktop\启动器\ui\home.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(1333, 730)
        Home.setMinimumSize(QtCore.QSize(1280, 730))
        self.verticalLayout = QtWidgets.QVBoxLayout(Home)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(1229, 595, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Select_Pass_ComboBox = ComboBox(Home)
        self.Select_Pass_ComboBox.setMinimumSize(QtCore.QSize(200, 50))
        self.Select_Pass_ComboBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Select_Pass_ComboBox.setObjectName("Select_Pass_ComboBox")
        self.horizontalLayout.addWidget(self.Select_Pass_ComboBox)
        spacerItem2 = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.Select_Mode_ComboBox = ComboBox(Home)
        self.Select_Mode_ComboBox.setMinimumSize(QtCore.QSize(120, 50))
        self.Select_Mode_ComboBox.setObjectName("Select_Mode_ComboBox")
        self.horizontalLayout.addWidget(self.Select_Mode_ComboBox)
        self.Start_PushButton = PrimaryPushButton(Home)
        self.Start_PushButton.setMinimumSize(QtCore.QSize(150, 50))
        self.Start_PushButton.setObjectName("Start_PushButton")
        self.horizontalLayout.addWidget(self.Start_PushButton)
        spacerItem3 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(1229, 47, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Form"))
        self.Select_Pass_ComboBox.setText(_translate("Home", "请选择账号"))
        self.Start_PushButton.setText(_translate("Home", "原神  启动"))
from qfluentwidgets import ComboBox, PrimaryPushButton
