# coding:utf-8
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import FluentIcon as FIF
from ui.setting_ui import Ui_setting
from qfluentwidgets import isDarkTheme, setTheme, Theme, MessageBox
from PyQt5.QtGui import QColor
from script import Tools
import os
import shutil
from script import OperationConfig, Call, ConfigPath
from tools import InfoBar, FileOperation

# 导入模块


# Setting UI 类
class Setting(Ui_setting, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # 初始化图标控件
        self.Theme_Icon.setIcon(FIF.PALETTE)
        self.Fix_Icon.setIcon(FIF.DEVELOPER_TOOLS)
        self.About_Icon.setIcon(FIF.HELP)
        # 初始化按钮图标
        self.AboutAuthor_Button.setIcon(FIF.GITHUB)
        self.AboutSponsor_Button.setIcon(FIF.LINK)
        self.AboutFeedback_Button.setIcon(FIF.FEEDBACK)
        # 初始化下拉列表控件
        self.ThemeNight_Button.checkedChanged.connect(lambda: self.SetDarKTheme())
        self.ThemeBg_Button.clicked.connect(lambda: self.SetBackgroundImage())
        self.FixGamePath_Button.clicked.connect(lambda: self.FixGetGamePath())

    def SetDarKTheme(self):
        if self.ThemeNight_Button.text == "关":
            if isDarkTheme():
                setTheme(Theme.LIGHT)
                self.Theme_Label.setTextColor(QColor(0, 0, 0))
                self.ThemeBg_Label.setTextColor(QColor(0, 0, 0))
                self.ThemeNight_Label.setTextColor(QColor(0, 0, 0))
                self.Fix_Label.setTextColor(QColor(0, 0, 0))
                self.FixGamePath_Label.setTextColor(QColor(0, 0, 0))
                self.FixSDK_Label.setTextColor(QColor(0, 0, 0))
                self.About_Label.setTextColor(QColor(0, 0, 0))
                self.AboutUpdate_Label.setTextColor(QColor(0, 0, 0))
                self.AboutFeedback_Label.setTextColor(QColor(0, 0, 0))
                self.AboutAuthor_Label.setTextColor(QColor(0, 0, 0))
                self.AboutSponsor_Label.setTextColor(QColor(0, 0, 0))
                self.update()
                InfoBar.Success(self, "切换成功", "现在已经是亮色模式了")
        else:
            if not isDarkTheme():
                setTheme(Theme.DARK)
                self.Theme_Label.setTextColor(QColor(255, 255, 255))
                self.ThemeBg_Label.setTextColor(QColor(255, 255, 255))
                self.ThemeNight_Label.setTextColor(QColor(255, 255, 255))
                self.Fix_Label.setTextColor(QColor(255, 255, 255))
                self.FixGamePath_Label.setTextColor(QColor(255, 255, 255))
                self.FixSDK_Label.setTextColor(QColor(255, 255, 255))
                self.About_Label.setTextColor(QColor(255, 255, 255))
                self.AboutUpdate_Label.setTextColor(QColor(255, 255, 255))
                self.AboutFeedback_Label.setTextColor(QColor(255, 255, 255))
                self.AboutAuthor_Label.setTextColor(QColor(255, 255, 255))
                self.AboutSponsor_Label.setTextColor(QColor(255, 255, 255))
                self.update()
                InfoBar.Success(self, "切换成功", "现在已经是暗色模式了")

    def SetBackgroundImage(self):
        new_file = Tools.SelectFile("请选择背景图片", "PNG Files|*.png;*.jpg;*.jpeg")

        if new_file:
            shutil.copyfile(new_file, "./rescourse/tmp.png")
            os.remove("./rescourse/background.png")
            os.rename("./rescourse/tmp.png", "./rescourse/background.png")
            InfoBar.Success(self, "更换成成", "背景图片更换成功")
        else:
            InfoBar.Warnning(
                self, "更换失败", "背景图片更换失败，你是不是不想换背景图片了？"
            )

    def FixSDK(self):
        # 修复PCGameSDK.dll
        if os.path.exists("./rescourse/PCGameSDK.dll"):
            GamePath = OperationConfig.GetGamePath(self)
            try:
                shutil.copyfile(
                    "./rescourse/PCGameSDK.dll",
                    GamePath + "\\YuanShen_Data\\Plugins\\tmp.dll",
                )
                if os.path.exists(GamePath + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll"):
                    os.remove(GamePath + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll")
                os.rename(
                    GamePath + "\\YuanShen_Data\\Plugins\\tmp.dll",
                    GamePath + "\\YuanShen_Data\\Plugins\\PCGameSDK.dll",
                )
                InfoBar.Success(self, "修复成功", "PCGameSDK.dll 补丁已打入")
            except Exception as e:
                InfoBar.Warnning(self, "修复失败", f"PCGameSDK.dll修复失败: {str(e)}")
        else:
            InfoBar.Warnning(
                self,
                "修复失败",
                "PCGameSDK.dll 补丁不存在，请检查 rescourse 文件夹是否完整",
            )
            
        # 修复BLPlatform64目录
        if os.path.exists("./rescourse/BLPlatform64"):
            GamePath = OperationConfig.GetGamePath(self)
            blplatform_path = GamePath + "\\YuanShen_Data\\Plugins\\BLPlatform64"
            try:
                # 如果目标目录已存在，先删除
                if os.path.exists(blplatform_path):
                    shutil.rmtree(blplatform_path)
                    
                # 复制整个目录
                shutil.copytree(
                    "./rescourse/BLPlatform64",
                    blplatform_path,
                )
                InfoBar.Success(self, "修复成功", "BLPlatform64 补丁已打入")
            except Exception as e:
                InfoBar.Warnning(self, "修复失败", f"BLPlatform64修复失败: {str(e)}")
        else:
            InfoBar.Warnning(self, "修复失败", "BLPlatform64 补丁不存在，请检查 rescourse 文件夹是否完整")

    def FixGetGamePath(self):
        GamePath = Tools.SelectFile("YuanShen.exe", "EXE Files |YuanShen.exe|")
        GamePath = GamePath[: GamePath.rfind("\\")]
        if not GamePath:
            InfoBar.Warnning(self, "更新游戏位置失败", "用户操作取消")
        Config = FileOperation.ReadJSon(ConfigPath)
        Config["Path"]["gamePath"] = GamePath
        FileOperation.WriteJson(ConfigPath, Config)
        if os.path.exists(GamePath):
            InfoBar.Success(self, "更新游戏位置成功", "现在就可以原神启动啦")
