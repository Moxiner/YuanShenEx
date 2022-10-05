'''
@ Created with PyCharm Community Edition And VSCode
@ Author Morbid And Moxiner
@ Date 2022/10/04
@ Time 20:47

@To Do:
✔ 选择文件并获取文件位置
🔧 安装 （复制文件到相应位置）
➕ 是否添加快捷方式
➕ 安装完成界面（InstallerStartButton 改变文字）

@Error:
❌ 文件位置报错
File: This File
Line: 89
FileNotFoundError: [Errno 2] No such file or directory: 'src\\PCGameSDK.dll' 
'''

import configparser
from fileinput import filename
from os import makedirs, path, symlink
from shutil import copyfile, copy, copytree
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from win32ui import CreateFileDialog
from win32api import MessageBox
from win32con import MB_OK
from Ui_gui import Ui_installer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
import sys

def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


        
###########################################################################
# 窗口启动


class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.ui = Ui_installer()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.m_Position = None
        self.ui.InstallerStart_Button.clicked.connect(self.installer)  # 绑定 InstallerStart_Button 点击事件
        self.ui.Look_Button.clicked.connect(self.choice_file)        # 绑定 Look_Button 点击事件
        self.show()

    # 拖动窗口
    def mousePressEvent(self, event):
        """获取鼠标相对窗口的位置"""
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        """更改窗口位置"""
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    

    def choice_file(self , *arg):
        '''选择文件'''
        MessageBox(0, "点击确定后在游戏目录：...(你的路径)\\Genshin Impact\\Genshin Impact Gam中选择YuanShen.exe文件，即可自动安装", "注意了注意了", MB_OK)
        lpsFilter = "EXE Files |YuanShen.exe|"
        dlg = CreateFileDialog(True, "YuanShen.exe", None, 0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        filename = dlg.GetPathName()  # 获取选择的⽂件名称
        filename = filename[:filename.rfind("\\")]
        self.ui.Path_LineEdit.setText(filename)

    def installer(self,*arg):
        '''安装'''
        filename = self.ui.Path_LineEdit.text() # 读取 Path_LineEdit 数据
        file = open(filename + "\\YuanSenEx.ini", 'w', encoding="UTF-8")
        file.write("[url]\n[public]\n[GunFu]\n[BFu]")
        file.close()
        config = configparser.ConfigParser()
        config.read(filename + "\\YuanSenEx.ini", encoding="UTF-8")
        config.set("url", "Path", filename)
        config.set("public", "game_version", "3.1.0")
        config.set("public", "plugin_sdk_version", "3.5.0")
        config.set("GunFu", "channel", "1")
        config.set("GunFu", "cps", "mihoyo")
        config.set("GunFu", "sub_channel", "1")
        config.set("BFu", "channel", "14")
        config.set("BFu", "cps", "bilibili")
        config.set("BFu", "sub_channel", "0")
        config.write(open(filename + "\\YuanSenEx.ini", "w", encoding="UTF-8"))

        copyfile("src\\PCGameSDK.dll", filename + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")
        if not path.exists(filename + "\\src"):
            makedirs(filename + "\\src")
        copyfile("src\\ico.ico", filename + "\\src\\ico.ico")
        copyfile("src\\background.png", filename + "\\src\\background.png")
        copyfile("src\\config.ini", filename + "\\config.ini")
        copyfile("src\\Launcher.exe", filename + "\\Launcher.exe")
        symlink(filename + "\\Launcher.exe", get_desktop() + "\\原神双服启动器")
        MessageBox(0, "安装完成", "提示", MB_OK)    
    
            

# 启动窗口
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = InstallerWindow()
    sys.exit(app.exec_())
