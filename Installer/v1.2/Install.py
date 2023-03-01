# @ Created with PyCharm Community Edition And VSCode
# @ Author Morbid And Moxiner
# @ Date 2022/10/04
# @ Time 20:47


from configparser import ConfigParser
from doctest import Example
from os import makedirs, path
from pathlib import Path
from shutil import copyfile
from tkinter import Label
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from win32ui import CreateFileDialog
from win32api import ShellExecute
from winshell import shortcut
from win32con import MB_OK
from wget import download
from Ui_Installer import Ui_installer
from Ui_Tip import Ui_tip
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
from sys import argv, exit
from threading import Thread

url_background = "http://www.moxiner.online:8888/down/Xwjj00dseqWo"
url_ico = "http://www.moxiner.online:8888/down/ZEvze0fecx3u"
url_config = "http://www.moxiner.online:8888/down/Xgt0CYjzjLCn"
url_Launcher = "https://wwu.lanzoue.com/iSgyv0ey1l6h"
url_pcgamesdk = "http://www.moxiner.online:8888/down/1BLkWFXjGPnF"
VERSION = "1.1.3"


def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER,
                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


def get_startMenu():
    key = OpenKey(HKEY_CURRENT_USER,
                  r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    return QueryValueEx(key, "Start Menu")[0]


def CreateLink(GamePath, targetPath):
    '''创建快捷方式
    参数:GamePath: 源目录
    targetPath:目标目录
    返回值:无
    '''
    with shortcut(targetPath + "\\原神启动器Ex.lnk") as link:
        link.path = GamePath + "\\Launcher.exe"
        link.working_directory = GamePath
# 窗口启动


class TipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.ui = Ui_tip()
        self.ui.setupUi(self)
        self.hide()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.m_Position = None

    def Message_Show(self, title, content):
        self.ui.Title_Label.setText(title)
        self.ui.Content_Label.setText(content)
        self.show()


class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.install_thread = Thread(target=self.installer_thread)
        self.m_flag = False
        self.ui = Ui_installer()
        self.ui.setupUi(self)
        self.ui.Title_Lable.setText("原神启动Ex安装程序 v" + VERSION)
        self.hide()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.m_Position = None
        self.GamePath = ""
        self.config_YunShenEx = ConfigParser()
        self.ui.Path_LineEdit.setReadOnly(True)  # 无法选中
        self.ui.InstallerStart_Button.clicked.connect(
            self.installer)  # 绑定 InstallerStart_Button 点击事件
        self.ui.Look_Button.clicked.connect(
            self.choice_file)  # 绑定 Look_Button 点击事件
        self.show()

    def hide(self):
        # 隐藏部件
        self.ui.InstallerEnd_Button.setEnabled(False)
        self.ui.InstallerEnd_Button.setHidden(True)
        self.ui.Progress_Frame.setHidden(True)

    def closeAndOpenLauncher(self):
        '''是否启动 Launcher 并关闭 Installer'''
        self.ui.InstallerEnd_Button.setEnabled(False)
        if self.ui.StartLauncher_CheckBox.isChecked():
            ShellExecute(0, 'open', self.LauncherPath +
                         "\\YuanShenEx\\Launcher.exe", '', self.LauncherPath + "\\YuanShenEx", 1)
        self.close()

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
        if QtCore.Qt.LeftButton and self.m_flag and self.m_Position.y() < 30:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def choice_file(self):
        # 选择文件点击事件
        # Message_Box("注意", "点击确定后在游戏目录：...(你的路径)\\Genshin Impact\\Genshin Impact Gam中选择YuanShen.exe文件，即可自动安装")
        lpsFilter = "EXE Files |YuanShen.exe|"
        dlg = CreateFileDialog(True, "YuanShen.exe", None,
                               0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        GamePath = dlg.GetPathName()  # 获取选择的⽂件名称
        GamePath = GamePath[:GamePath.rfind("\\")]
        self.ui.Path_LineEdit.setText(GamePath)

    def installer(self):
        # 安装点击事件
        self.GamePath = self.ui.Path_LineEdit.text()  # 读取 Path_LineEdit 数据

        if len(self.GamePath) == 0:
            tip.Message_Show("错误", "请先选择游戏路径")
            return
        self.LauncherPath = path.abspath(path.dirname(self.GamePath))
        self.ui.Installer_Label.setEnabled(True)  # 无法使用
        self.ui.InstallerStart_Button.setEnabled(False)  # 无法使用
        self.ui.InstallerStart_Button.setHidden(True)
        self.ui.InstallerEnd_Button.setVisible(False)
        self.ui.Top_Right_Frame.setEnabled(False)
        self.ui.Top_Right_Frame.setHidden(True)
        self.ui.Bottom_Installer_Frame.resize(730, 80)
        self.ui.Progress_ProgressBox.setTextVisible(False)
        self.ui.Progress_ProgressBox.setValue(0)
        self.ui.Progress_Frame.setHidden(False)
        QApplication.processEvents()  # 刷新界面


        # 判断并创建src目录
        if not path.exists(self.LauncherPath + "\\YuanShenEx\\src"):
            makedirs(self.LauncherPath + "\\YuanShenEx\\src")
        # 判断并创建src目录

        # 添加YuanShenEx.ini文件
        if not path.exists(self.LauncherPath + "\\YuanShenEx\\src"):
            makedirs(self.LauncherPath + "\\YuanShenEx\\src")
        file = open(self.LauncherPath + "\\YuanShenEx\\YuanShenEx.ini", 'w', encoding="UTF-8")
        file.write("[url]\n[public]\n[GuanFu]\n[BFu]")
        file.close()
        self.config_YunShenEx.read(
            self.LauncherPath + "\\YuanShenEx\\YuanShenEx.ini", encoding="UTF-8")
        self.config_YunShenEx.set("url", "GamePath", self.GamePath)
        self.config_YunShenEx.set("public", "game_version", "3.1.0")
        self.config_YunShenEx.set("public", "plugin_sdk_version", "3.5.0")
        self.config_YunShenEx.set("GuanFu", "channel", "1")
        self.config_YunShenEx.set("GuanFu", "cps", "mihoyo")
        self.config_YunShenEx.set("GuanFu", "sub_channel", "1")
        self.config_YunShenEx.set("BFu", "channel", "14")
        self.config_YunShenEx.set("BFu", "cps", "bilibili")
        self.config_YunShenEx.set("BFu", "sub_channel", "0")
        self.config_YunShenEx.write(
            open(self.LauncherPath + "\\YuanShenEx\\YuanShenEx.ini", "w", encoding="UTF-8"))
        self.ui.Progress_ProgressBox.setValue(10)


            # 如果ini不存在则创建
        if not path.exists(self.LauncherPath + "\\YuanShenEx\\src\\config.ini"):
            file = open(self.LauncherPath + "\\YuanShenEx\\src\\config.ini",
                        'w', encoding="UTF-8")
            file.write("[General]")
            file.close()

        # 从YuanShenEx.ini读取数据写入config.ini文件
        config_config = ConfigParser()
        config_config.read(self.GamePath + "\\config.ini", encoding="UTF-8")
        config_config.set("General", "channel",
                          self.config_YunShenEx.get("GuanFu", "channel"))
        config_config.set("General", "cps",
                          self.config_YunShenEx.get("GuanFu", "cps"))
        config_config.set("General", "game_version",
                          self.config_YunShenEx.get("public", "game_version"))
        config_config.set("General", "sub_channel",
                          self.config_YunShenEx.get("GuanFu", "sub_channel"))
        config_config.set("General", "plugin_sdk_version",
                          self.config_YunShenEx.get("public", "plugin_sdk_version"))
        config_config.write(
            open(self.GamePath + "\\config.ini", "w", encoding="UTF-8"))
        # 多线程下载
        self.ui.Progress_ProgressBox.setValue(20)
        self.install_thread.start()
        self.install_thread.join()



        # 创建桌面快捷方式
        if self.ui.CreateStartedLink_CheckBox.isChecked():
            CreateLink(self.LauncherPath + "\YuanShenEx", get_startMenu())
        # 创建开始菜单快捷方式
        if self.ui.CreateDesktopLink_CheckBox.isChecked():
            CreateLink(self.LauncherPath + "\YuanShenEx", get_desktop())

    def installer_thread(self):
        self.m_flag = False
        # 复制PCGameSDK.dll文件
        try:
            copyfile("src\\PCGameSDK.dll", self.GamePath +
                     "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")
            copyfile("src\\PCGameSDK.dll", self.LauncherPath +
                     "\\YuanShenEx\\src\\PCGameSDK.dll")
        except FileNotFoundError as result:
            # 打印错误信息
            download(url_pcgamesdk,
                     self.LauncherPath + "\\YuanShenEx\\src\\PCGameSDK.dll" ,bar=None)
            copyfile(self.LauncherPath + "\\YuanShenEx\\src\\PCGameSDK.dll",
                     self.GamePath + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")


        self.ui.Progress_ProgressBox.setValue(40)

        # 复制ico.ico文件
        try:
            copyfile("\\YuanShenEx\\src\\ico.ico", self.LauncherPath + "\\YuanShenEx\\src\\ico.ico" )
        except FileNotFoundError as result:
            # 打印错误信息
            download(url_ico,
                     self.LauncherPath + "\\YuanShenEx\\src\\ico.ico" , bar=None)
        self.ui.Progress_ProgressBox.setValue(60)


        # 复制background.png
        try:
            copyfile("src\\background.png", self.LauncherPath +
                     "\\YuanShenEx\\src\\background.png")
        except FileNotFoundError as result:
            
            # 打印错误信息
            download(url_background,
                     self.LauncherPath + "\\YuanShenEx\\src\\background.png" , bar=None)
        self.ui.Progress_ProgressBox.setValue(80)

        # 复制Launcher.exe启动器
        try:
            copyfile("src\\Launcher.exe", self.LauncherPath + "\\YuanShenEx\\Launcher.exe")
        except FileNotFoundError as result:
            
            # 打印错误信息
            download(url_Launcher,
                     self.LauncherPath + "\\YuanShenEx\\Launcher.exe" , bar=None)
        # 复制config.exe启动器
        try:
            copyfile("src\\config.ini", self.LauncherPath + "\\YuanShenEx\\src\\config.ini")
        except FileNotFoundError as result:
            
            # 打印错误信息
            download(url_config,
                     self.LauncherPath + "\\YuanShenEx\\src\\config.ini" , bar=None)
        self.ui.Progress_ProgressBox.setValue(100)
        self.ui.Progress_Label.setText("安装完成")
        self.ui.Bottom_Installer_Frame.resize(730, 110)
        self.ui.InstallerEnd_Button.setVisible(True)
        self.ui.InstallerEnd_Button.setEnabled(True)
        self.ui.Top_Right_Frame.setEnabled(True)
        self.ui.Top_Right_Frame.setHidden(False)
        self.ui.InstallerEnd_Button.clicked.connect(self.closeAndOpenLauncher)


# 创建对象，调用创建主窗口方法，进去消息循环
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(argv)
    win = InstallerWindow()
    tip = TipWindow()
    exit(app.exec_())
