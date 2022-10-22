from fileinput import close
from tkinter import Menu
from turtle import left
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui , Qt
from Ui_Launcher import Ui_LauncherWindow
from Script import *
from sys import argv, exit


class Ui_Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.ui = Ui_LauncherWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.m_Position = None
        self.KeyBinding()
        self.show()
        self.HideSet()
        self.MenuStatus = None

    
    
    def mousePressEvent(self, event):
        MouseMove.mousePressEvent(self, event)
    def mouseMoveEvent(self, mouse_event):
        MouseMove.mouseMoveEvent(self, mouse_event)
    def mouseReleaseEvent(self, mouse_event):
        MouseMove.mouseReleaseEvent(self, mouse_event)


    def HideSet(self):
        self.ui.SetFrame.move(-400 ,0)
        self.ui.APPFrame.move(-251 ,0)
        self.ui.FixedFrame.move(-391 ,0)
        

    def KeyBinding(self):
        self.ui.Start_PushButton.clicked.connect(lambda: Call.Start(self))
        self.ui.Close_Buttom.clicked.connect(self.close)
        self.ui.Min_Bottom.clicked.connect(self.showMinimized)
        self.ui.Fixed_Button.clicked.connect(lambda:Call.CallFixedButton(self))
        self.ui.APP_Button.clicked.connect(lambda:Call.CallAPPButton(self))
        self.ui.Set_Button.clicked.connect(lambda:Call.CallSetButton(self))
        

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(argv)
    Launcher = Ui_Launcher()
    exit(app.exec_())
