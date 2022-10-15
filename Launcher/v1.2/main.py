from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
from Ui_Launcher import Ui_LauncherWindow
import Script
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
        self.show()
    
    
    def mousePressEvent(self, event):
       Script.MouseMove.mousePressEvent(self, event)
    def mouseMoveEvent(self, mouse_event):
        Script.MouseMove.mouseMoveEvent(self, mouse_event)
    def mouseReleaseEvent(self, mouse_event):
        Script.MouseMove.mouseReleaseEvent(self, mouse_event)



if __name__ == "__main__":
    
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(argv)
    Launcher = Ui_Launcher()
    exit(app.exec_())
