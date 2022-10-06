# @ Created with PyCharm Community Edition And VSCode
# @ Author Morbid And Moxiner
# @ Date 2022/10/04
# @ Time 20:47

# @To Do:
# ✔ 选择文件并获取文件位置
# 🔧 安装 （复制文件到相应位置）
# ➕ 是否添加快捷方式
# ➕ 安装完成界面（InstallerStartButton 改变文字）

from configparser import ConfigParser
from os import makedirs, path, symlink
from shutil import copyfile
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from win32ui import CreateFileDialog
from win32api import MessageBox
from win32con import MB_OK
from Ui_Installer import Ui_installer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui
import sys


def get_desktop():
    key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, "Desktop")[0]


def Message_Box(title, src):
    MessageBox(0, src, title, MB_OK)


# 窗口启动


class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.m_flag = False
        self.ui = Ui_installer()
        self.ui.setupUi(self)
        self.hide()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.m_Position = None
        self.ui.InstallerStart_Button.clicked.connect(self.installer)  # 绑定 InstallerStart_Button 点击事件
        self.ui.Look_Button.clicked.connect(self.choice_file)  # 绑定 Look_Button 点击事件
        self.show()


    def hide(self):
        '''隐藏部件'''
        self.ui.InstallerEnd_Button.setEnabled(False)
        self.ui.InstallerEnd_Button.setHidden(True)

    # 拖动窗口
    def mousePressEvent(self, event):
        """获取鼠标相对窗口的位置"""
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        # 更改窗口位置
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def choice_file(self):
        # 选择文件点击事件
        # Message_Box("注意", "点击确定后在游戏目录：...(你的路径)\\Genshin Impact\\Genshin Impact Gam中选择YuanShen.exe文件，即可自动安装")
        lpsFilter = "EXE Files |YuanShen.exe|"
        dlg = CreateFileDialog(True, "YuanShen.exe", None, 0x04 | 0x02, lpsFilter)  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(get_desktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        fileName = dlg.GetPathName()  # 获取选择的⽂件名称
        fileName = fileName[:fileName.rfind("\\")]
        self.ui.Path_LineEdit.setText(fileName)

    def installer(self):
        # 安装点击事件
        fileName = self.ui.Path_LineEdit.text()  # 读取 Path_LineEdit 数据
        if len(fileName) == 0:
            Message_Box("错误", "请先选择游戏路径")
            return

        # 添加YuanSenEx.ini文件
        self.ui.InstallerStart_Button.setVisible(False)
        self.ui.Bottom_Installer_Frame.setVisible(False)

        file = open(fileName + "\\YuanSenEx.ini", 'w', encoding="UTF-8")
        file.write("[url]\n[public]\n[GuanFu]\n[BFu]")
        file.close()
        config_YunShenEx = ConfigParser()
        config_YunShenEx.read(fileName + "\\YuanSenEx.ini", encoding="UTF-8")
        config_YunShenEx.set("url", "Path", fileName)
        config_YunShenEx.set("public", "game_version", "3.1.0")
        config_YunShenEx.set("public", "plugin_sdk_version", "3.5.0")
        config_YunShenEx.set("GuanFu", "channel", "1")
        config_YunShenEx.set("GuanFu", "cps", "mihoyo")
        config_YunShenEx.set("GuanFu", "sub_channel", "1")
        config_YunShenEx.set("BFu", "channel", "14")
        config_YunShenEx.set("BFu", "cps", "bilibili")
        config_YunShenEx.set("BFu", "sub_channel", "0")
        config_YunShenEx.write(open(fileName + "\\YuanSenEx.ini", "w", encoding="UTF-8"))

        # 复制PCGameSDK.dll文件
        try:
            copyfile("src\\PCGameSDK.dll", fileName + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")
        except Exception as result:
            # 打印错误信息
            print(result)

        # 判断并创建src目录
        if not path.exists(fileName + "\\src"):
            makedirs(fileName + "\\src")

        # 复制ico.ico文件
        try:
            copyfile("src\\ico.ico", fileName + "\\src\\ico.ico")
        except Exception as result:
            # 打印错误信息
            print(result)

        # 复制background.png
        try:
            copyfile("src\\background.png", fileName + "\\src\\background.png")
        except Exception as result:
            # 打印错误信息
            print(result)

        # 如果ini不存在则创建
        if not path.exists(fileName + "\\config.ini"):
            file = open(fileName + "\\config.ini", 'w', encoding="UTF-8")
            file.write("[General]")
            file.close()

        # 从YuanSenEx.ini读取数据写入config.ini文件
        config_config = ConfigParser()
        config_config.read(fileName + "\\config.ini", encoding="UTF-8")
        config_config.set("General", "channel", config_YunShenEx.get("GuanFu", "channel"))
        config_config.set("General", "cps", config_YunShenEx.get("GuanFu", "cps"))
        config_config.set("General", "game_version", config_YunShenEx.get("public", "game_version"))
        config_config.set("General", "sub_channel", config_YunShenEx.get("GuanFu", "sub_channel"))
        config_config.set("General", "plugin_sdk_version", config_YunShenEx.get("public", "plugin_sdk_version"))
        config_config.write(open(fileName + "\\config.ini", "w", encoding="UTF-8"))

        # 复制Launcher.exe启动器
        try:
            copyfile("src\\Launcher.exe", fileName + "\\Launcher.exe")
        except Exception as result:
            # 打印错误信息
            print(result)

        # 创建桌面快捷方式
        if self.ui.CreateStartedLink_CheckBoc.isChecked():
            symlink(fileName + "\\Launcher.exe", get_desktop() + "\\原神双服启动器")

        # 创建开始菜单快捷方式
        if self.ui.CreateDesktopLink_CheckBox.isChecked():
            pass
        self.ui.InstallerEnd_Button.setHidden(False)
        # Message_Box("提示", "安装完成")
        self.ui.InstallerEnd_Button.setEnabled(True)

# 创建对象，调用创建主窗口方法，进去消息循环
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = InstallerWindow()
    sys.exit(app.exec_())
