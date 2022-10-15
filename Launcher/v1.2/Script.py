from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui


class MouseMove:
        # 拖动窗口
    def mousePressEvent(self, event):
        """获取鼠标相对窗口的位置"""
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        # 更改窗口位置
        if QtCore.Qt.LeftButton and self.m_flag and self.m_Position.y() < 50:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
