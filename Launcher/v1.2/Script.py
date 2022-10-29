from multiprocessing.sharedctypes import Value
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui ,Qt
import configparser
import json
import os
from win32ui import CreateFileDialog
from win32api import ShellExecute
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER


ConfigPath = "YuanShenEx.json"
Config = '''{
    "Url":{
        "PCgameSDK":"",
        "Background":"",
        "ico":"",
        "Launcher":"",
        "GuojiFu":""
    },
    "Path":{
        "launcherPath":"None",
        "gamePath":"None"
    },
    "Account":[
        {
            "name":"默认","path":"None"}],"Plugins":{"刻师傅工具箱":{"downlorad":"","run":"","path":""},"空莹酒馆原神地图":{"downlorad":"","run":"","path":""}},"Setting":{"run":1}}
'''



class Event:
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

    def showWindows(self ,event):
        """显示窗口的动画"""
        self.anim = Qt.QPropertyAnimation(self.ui.Main_Widget, b"geometry") 
        self.anim.setDuration(500)
        self.anim.setStartValue(Qt.QRect(0, 0, 981, 0))   
        self.anim.setEndValue(Qt.QRect(0, 0, 981, 571)) 
        self.anim.setEasingCurve(Qt.QEasingCurve.InQuint)
        self.anim.start() 
    def HideWindows(self ,event):
        """隐藏窗口的动画"""
        self.anim = Qt.QPropertyAnimation(self.ui.Main_Widget, b"geometry") 
        self.anim.setDuration(500)
        self.anim.setStartValue(Qt.QRect(0, 0, 981, 571))   
        self.anim.setEndValue(Qt.QRect(0, 0, 981, 0)) 
        self.anim.finished.connect(self.showMinimized)
        self.anim.setEasingCurve(Qt.QEasingCurve.OutQuint)
        self.anim.start()

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
        Path = dlg.Path()  # 获取选择的⽂件名称
        Path = Path[:Path.rfind("\\")]
        return Path

class OperationConfig:
    def ReadConfig(file):
        try:
            with open(file , encoding="utf8") as f:
                Config = json.loads(f.read())
            return Config
        except Exception:
            OperationConfig.InitConfig()

    
    def WriteConfig(file , date):
        with open(file ,mode="w+", encoding="utf8") as f:
            Config = json.dumps(date)
            f.write(Config)

    def InitConfig():
        if not os.path.exists(ConfigPath):
            OperationConfig.WriteConfig(ConfigPath , Config)

    def GetGamePath():
        Config = OperationConfig.ReadConfig(ConfigPath)
        return Config
            

        


class Switch:
    def mihoyo():
            '''将配置文件改成官服配置并启动游戏'''
            GamePath = OperationConfig.ReadConfig(ConfigPath)["Path"]["gamePath"]
            config = configparser.ConfigParser()
            config.read(GamePath + "/config.ini" , encoding="utf8")
            config.set("General", "channel", "1")
            config.set("General", "cps", "mihoyo")
            config.set("General", "sub_channel", "1")
            config.write(open(GamePath + "/config.ini", "w"))



    def bilibili():
        '''将配置文件改成B服配置并启动游戏'''
        GamePath = OperationConfig.ReadConfig(ConfigPath)["Path"]["gamePath"]
        config = configparser.ConfigParser()
        config.read(GamePath + "/config.ini", encoding="utf8")
        config.set("General", "channel", "14")
        config.set("General", "cps", "bilibili")
        config.set("General", "sub_channel", "0")
        config.write(open(GamePath + "/config.ini", "w"))
            

        

class Call:
    def Start(self):
        GamePath = OperationConfig.ReadConfig(ConfigPath)["Path"]["gamePath"]
        if GamePath == "":
            pass
        elif self.ui.Mode_ComboBox.currentText() == "启动官服":
            Switch.Guanfu()
        elif self.ui.Mode_ComboBox.currentText() == "启动B服":
            Switch.BiliBili()
        elif self.ui.Mode_ComboBox.currentText() == "启动国际服":
            Switch.GuoJifu()
        ShellExecute(0, 'open', GamePath  + "/YuanShen.exe" , '' , GamePath , 1)    

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

