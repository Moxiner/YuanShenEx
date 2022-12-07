from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, Qt

def ShowFixedFrameAnim(self):
    self.post_Anim = Qt.QPropertyAnimation(self.ui.FixedFrame, b"geometry")
    self.post_Anim.setDuration(300)
    self.post_Anim.setStartValue(Qt.QRect(-361, 0, 361, 521))   # 设置起始大小
    self.post_Anim.setEndValue(Qt.QRect(0, 0, 361, 521))   # 设置终止大小
    self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
    self.post_Anim.start()
    MenuStatus = "FixedFrame"
    return MenuStatus

def ShowAPPFrameAnim(self):
    self.post_Anim = Qt.QPropertyAnimation(self.ui.APPFrame, b"geometry")
    self.post_Anim.setDuration(500)
    self.post_Anim.setStartValue(Qt.QRect(-231, 0, 231, 521))   # 设置起始大小
    self.post_Anim.setEndValue(Qt.QRect(0, 0, 231, 521))   # 设置终止大小
    self.post_Anim.start()
    self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
    MenuStatus = "APPFrame"
    return MenuStatus

def ShowSetFrameAnim(self):
    self.post_Anim = Qt.QPropertyAnimation(self.ui.SetFrame, b"geometry")
    self.post_Anim.setDuration(500)
    self.post_Anim.setStartValue(Qt.QRect(-391, 0, 391, 521))   # 设置起始大小
    self.post_Anim.setEndValue(Qt.QRect(0, 0, 391, 521))   # 设置终止大小
    self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
    self.post_Anim.start()
    MenuStatus = "SetFrame"
    return MenuStatus

def HideFixedFrameAnim(self):
    if self.MenuStatus == "FixedFrame":
        # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
        self.post_Anim = Qt.QPropertyAnimation(
            self.ui.FixedFrame, b"geometry")
        self.post_Anim.setDuration(300)   # 设定动画时间
        self.post_Anim.setStartValue(Qt.QRect(0, 0, 361, 521))   # 设置起始大小
        self.post_Anim.setEndValue(Qt.QRect(-361, 0, 361, 521))   # 设置终止大小
        self.post_Anim.setEasingCurve(Qt.QEasingCurve.InQuint)
        self.post_Anim.start()
        MenuStatus = None
        return MenuStatus
def HideSetFrameAnim(self):
        # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
        self.post_Anim = Qt.QPropertyAnimation(
            self.ui.APPFrame, b"geometry")
        self.post_Anim.setDuration(300)   # 设定动画时间
        self.post_Anim.setStartValue(Qt.QRect(0, 0, 231, 521))   # 设置起始大小
        self.post_Anim.setEndValue(Qt.QRect(-231, 0, 231, 521))   # 设置终止大小
        self.post_Anim.setEasingCurve(Qt.QEasingCurve.InQuint)
        self.post_Anim.start()
        MenuStatus = None
        return MenuStatus
