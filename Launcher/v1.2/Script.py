from mimetypes import init
from multiprocessing.sharedctypes import Value
from operator import mod
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui ,Qt
import configparser
from os import makedirs, path
from win32ui import CreateFileDialog
from win32api import ShellExecute
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER


ConfigPath = "YuanShen.ini"

class MouseMove:
    # 拖动窗口
    def mousePressEvent(self, event):
        """获取鼠标相对窗口的位置"""
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, mouse_event):
        # 更改窗口位置
        if QtCore.Qt.LeftButton and self.m_flag and self.m_Position.y() < 50:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

class Tools:
    def GetDesktop():
        key = OpenKey(HKEY_CURRENT_USER,
                    r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return QueryValueEx(key, "Desktop")[0]
    
    def SelectFile(file ,description):
        dlg = CreateFileDialog(True, file, None,
                            0x04 | 0x02 , description)  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(Tools.GetDesktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        GamePath = dlg.GetPathName()  # 获取选择的⽂件名称
        GamePath = GamePath[:GamePath.rfind("\\")]
        return GamePath

            

class OperationConfig:
    def IOConfig(file, mode , section, option, value = None):
        InitConfig.InitYuanShen()
        config = configparser.ConfigParser()
        config.read(file ,encoding="utf8")
        if mode == "r":
            return config.get(section, option)
        elif mode == "w":
            config.set(section, option, value)
            config.write(open(file, "w"))


class InitConfig:

    def InitYuanShen():
        if not path.exists("src"):
            makedirs("src")
        if not path.exists(ConfigPath):
            file = open(ConfigPath, 'w', encoding="UTF-8")
            file.write("[Path\n[Account]\n[Setting]")
            OperationConfig.IOConfig(ConfigPath , "w" ,"Path" , "GamePath" , "" ) 
            file.close()

    def GetGamePath():
        try:
            GamePath = OperationConfig.IOConfig(ConfigPath ,"r", "Path" , "GamePath")
            return GamePath
        except Exception:
            GamePath = Tools.SelectFile( "YuanShen.exe" , "EXE File |YuanShen.exe|")
            OperationConfig.IOConfig(ConfigPath ,"w", "Path" , "GamePath" , GamePath)
            return GamePath



class Switch:
    def Guanfu():
        file = InitConfig.GetGamePath() + "/config.ini"
        OperationConfig.IOConfig(file, "w" ,"General", "channel", "1")
        OperationConfig.IOConfig(file, "w" , "General", "cps", "mihoyo")
        OperationConfig.IOConfig(file, "w" , "General", "sub_channel", "1")

    def BiliBili():
        file = InitConfig.GetGamePath() + "/config.ini"
        OperationConfig.IOConfig(file, "w" ,"General", "channel", "14")
        OperationConfig.IOConfig(file, "w" , "General", "cps", "bilibili")
        OperationConfig.IOConfig(file, "w" , "General", "sub_channel", "0")

    def GuoJifu():
        file = InitConfig.GetGamePath() + "/config.ini"
        OperationConfig.IOConfig(file, "w" ,"General", "channel", "14")
        OperationConfig.IOConfig(file, "w" , "General", "cps", "bilibili")
        OperationConfig.IOConfig(file, "w" , "General", "sub_channel", "0")
    

class Call:
    def Start(self):
        if InitConfig.GetGamePath() == "":
            pass
        elif self.ui.Mode_ComboBox.currentText() == "启动官服":
            Switch.Guanfu()
        elif self.ui.Mode_ComboBox.currentText() == "启动B服":
            Switch.BiliBili()
        elif self.ui.Mode_ComboBox.currentText() == "启动国际服":
            Switch.GuoJifu()
        ShellExecute(0, 'open', InitConfig.GetGamePath()  + "/YuanShen.exe" , '' , InitConfig.GetGamePath() , 1)    
    def CallFixedButton(self):
        if self.MenuStatus == None:
            MenuStatus = Anim.ShowFixedFrameAnim(self)
        elif self.MenuStatus == "FixedFrame":
            MenuStatus = Anim.HideFrameAnim(self)
        else:
            Anim.HideFrameAnim(self)
            MenuStatus = Anim.ShowFixedFrameAnim(self)
        self.MenuStatus = MenuStatus
    def CallAPPButton(self):
        if self.MenuStatus == None:
            MenuStatus = Anim.ShowAPPFrameAnim(self)
        elif self.MenuStatus != None:
            MenuStatus = Anim.HideFrameAnim(self)
        self.MenuStatus = MenuStatus

    def CallSetButton(self):
        if self.MenuStatus == None:
            MenuStatus = Anim.ShowSetFrameAnim(self)
        elif self.MenuStatus != None:
            MenuStatus = Anim.HideFrameAnim(self)
        self.MenuStatus = MenuStatus






class Anim:
    def ShowFixedFrameAnim(self):
        self.post_Anim = Qt.QPropertyAnimation(self.ui.FixedFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
        self.post_Anim.setDuration(300)   
        self.post_Anim.setStartValue(Qt.QRect(-361, 0, 361, 521))   # 设置起始大小
        self.post_Anim.setEndValue(Qt.QRect(0, 0, 361, 521))   # 设置终止大小
        self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
        self.post_Anim.start()
        MenuStatus = "FixedFrame"
        return MenuStatus 
    def ShowAPPFrameAnim(self):
        self.post_Anim = Qt.QPropertyAnimation(self.ui.APPFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
        self.post_Anim.setDuration(500)   
        self.post_Anim.setStartValue(Qt.QRect(-231, 0, 231, 521))   # 设置起始大小
        self.post_Anim.setEndValue(Qt.QRect(0, 0, 231, 521))   # 设置终止大小
        self.post_Anim.start()
        self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
        MenuStatus = "APPFrame"
        return MenuStatus
    def ShowSetFrameAnim(self):
        self.post_Anim = Qt.QPropertyAnimation(self.ui.SetFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
        self.post_Anim.setDuration(500)   
        self.post_Anim.setStartValue(Qt.QRect(-391, 0, 391, 521))   # 设置起始大小
        self.post_Anim.setEndValue(Qt.QRect(0, 0, 391, 521))   # 设置终止大小
        self.post_Anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
        self.post_Anim.start()
        MenuStatus = "SetFrame"
        return MenuStatus


    def HideFrameAnim(self):
        if self.MenuStatus == "FixedFrame":
            self.post_Anim = Qt.QPropertyAnimation(self.ui.FixedFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
            self.post_Anim.setDuration(300)   # 设定动画时间
            self.post_Anim.setStartValue(Qt.QRect(0, 0, 361, 521))   # 设置起始大小
            self.post_Anim.setEndValue(Qt.QRect(-361, 0, 361, 521))   # 设置终止大小
            self.post_Anim.setEasingCurve(Qt.QEasingCurve.InQuint)
            self.post_Anim.start()
        if self.MenuStatus == "APPFrame":
            self.post_Anim = Qt.QPropertyAnimation(self.ui.APPFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
            self.post_Anim.setDuration(300)   # 设定动画时间
            self.post_Anim.setStartValue(Qt.QRect(0, 0, 231, 521))   # 设置起始大小
            self.post_Anim.setEndValue(Qt.QRect(-231, 0, 231, 521))   # 设置终止大小
            self.post_Anim.setEasingCurve(Qt.QEasingCurve.InQuint)
            self.post_Anim.start()
        if self.MenuStatus == "SetFrame":
            self.post_Anim = Qt.QPropertyAnimation(self.ui.SetFrame, b"geometry")   # 参数self.listView就是要进行动画设置的组件，用返回的对象来进行设置
            self.post_Anim.setDuration(300)   # 设定动画时间
            self.post_Anim.setStartValue(Qt.QRect(0, 0, 391, 521))   # 设置起始大小
            self.post_Anim.setEndValue(Qt.QRect(-391, 0, 391, 521))   # 设置终止大小
            self.post_Anim.setEasingCurve(Qt.QEasingCurve.InQuint)
            self.post_Anim.start()
        MenuStatus = None
        return MenuStatus