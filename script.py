from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, Qt
import configparser
from qfluentwidgets import MessageBox
import os
from win32ui import CreateFileDialog
from win32api import ShellExecute
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
import configparser
import shutil
from tools import FileOperation, InfoBar

ConfigPath = "setting/YuanShenEx.json"

Config = {
    "Path": {"launcherPath": "", "gamePath": ""},
    "Account": {
        "BFu": [{"name": "默认", "path": ""}],
        "GuanFu": [{"name": "默认", "path": ""}],
    },
}


class Switch:
    def Guanfu():
        """将配置文件改成官服配置并启动游戏"""
        GamePath = FileOperation.ReadJSon(ConfigPath)["Path"]["gamePath"]
        config = configparser.ConfigParser()
        config.read(GamePath + "/config.ini", encoding="utf8")
        config.set("General", "channel", "1")
        config.set("General", "cps", "gw_PC")
        # config.set("General", "sub_channel", "1")
        config.write(open(GamePath + "/config.ini", "w"))

    def BiliBili():
        """将配置文件改成B服配置并启动游戏"""
        GamePath = FileOperation.ReadJSon(ConfigPath)["Path"]["gamePath"]
        config = configparser.ConfigParser()
        config.read(GamePath + "/config.ini", encoding="utf8")
        config.set("General", "channel", "14")
        config.set("General", "cps", "bilibili")
        # config.set("General", "sub_channel", "0")
        config.write(open(GamePath + "/config.ini", "w"))


class Tools:
    def GetDesktop():
        key = OpenKey(
            HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        )
        return QueryValueEx(key, "Desktop")[0]

    def SelectFile(file, description):
        dlg = CreateFileDialog(
            True, file, None, 0x04 | 0x02, description
        )  # 1表⽰打开⽂件对话框
        dlg.SetOFNInitialDir(Tools.GetDesktop())  # 设置打开⽂件对话框中的初始显⽰⽬录
        dlg.DoModal()
        Path = dlg.GetPathName()  # 获取选择的⽂件名称
        return Path


class OperationConfig:
    def InitConfig():
        if not os.path.exists(ConfigPath):
            FileOperation.CreateJson(ConfigPath, Config)

    def GetGamePath(self):
        from demo import Window

        Config = FileOperation.ReadJSon(ConfigPath)
        Config = Config["Path"]["gamePath"]
        if not os.path.exists(Config):
            Window.ShowGetGamePathMessage(self)
            Tmp = FileOperation.ReadJSon(ConfigPath)
            Config = Tmp["Path"]["gamePath"]
        return Config


class Call:
    def SelectGamePath():
        GamePath = Tools.SelectFile("YuanShen.exe", "EXE Files |YuanShen.exe|")
        GamePath = GamePath[: GamePath.rfind("\\")]
        if not GamePath:
            pass
        Config = FileOperation.ReadJSon(ConfigPath)
        Config["Path"]["gamePath"] = GamePath
        FileOperation.WriteJson(ConfigPath, Config)

    def Start(self):
        from demo import Window

        GamePath = OperationConfig.GetGamePath(self)
        # 配置游戏配置文件
        if not GamePath or not os.path.exists(GamePath):
            InfoBar.Warnning(self, "启动失败", "未找到对应路径")
            return

        if self.home.Select_Mode_ComboBox.currentText() == "启动官服":
            Switch.Guanfu()
        elif self.home.Select_Mode_ComboBox.currentText() == "启动B服":
            Switch.BiliBili()
        else:
            # 如果没有选择有效的模式，则不启动游戏
            InfoBar.Warnning(self, "启动失败", "请选择有效的启动模式")
            return

        # 检查并复制PCGameSDK.dll文件
        dll_path = GamePath + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll"
        if not os.path.exists(dll_path):
            source_dll = "./rescourse/PCGameSDK.dll"
            if os.path.exists(source_dll):
                try:
                    shutil.copyfile(source_dll, dll_path)
                except Exception as e:
                    InfoBar.Warnning(
                        self, "复制文件失败", f"无法复制PCGameSDK.dll: {str(e)}"
                    )
                    return

        # 检查并复制BLPlatform64目录
        blplatform_path = GamePath + "\\YuanShen_Data\\Plugins\\BLPlatform64"
        if not os.path.exists(blplatform_path):
            source_dir = "./rescourse/BLPlatform64"
            if os.path.exists(source_dir):
                try:
                    shutil.copytree(source_dir, blplatform_path)
                except Exception as e:
                    InfoBar.Warnning(
                        self, "复制目录失败", f"无法复制BLPlatform64: {str(e)}"
                    )
                    return

        # 启动游戏
        try:
            ShellExecute(0, "open", GamePath + "/YuanShen.exe", "", GamePath, 1)
            Window.showMinimized(self)
        except Exception as e:
            InfoBar.Warnning(self, "启动失败", f"无法启动游戏: {str(e)}")
