# coding:utf-8

import sys
from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (
    MessageBox,
    SplitFluentWindow,
    FluentTranslator,
    setTheme,
    isDarkTheme,
    Theme,
    NavigationItemPosition,
)
from qfluentwidgets import FluentIcon as FIF
from home import Home
from setting import Setting
from account import Account
from script import Call
from qfluentwidgets import SplashScreen


class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.home = Home(self)
        self.setting = Setting(self)
        # self.account = Account(self)
        self.setWindowIcon(QIcon("./rescourse/ico.ico"))
        self.setWindowTitle("原神启动器Ex Dev 2.1.0")
        self.show()
        self.initNavigation()
        self.initWindow()
        self.home.Start_PushButton.clicked.connect(lambda: Call.Start(self))
        self.setting.FixSDK_Button.clicked.connect(lambda: self.setting.FixSDK())
        self.setting.AboutUpdate_Button.clicked.connect(
            lambda: MessageBox(
                "检查更新功能还没做捏", "要不你到QQ群里看看?", self
            ).exec()
        )
        self.setting.AboutAuthor_Button.clicked.connect(
            lambda: MessageBox(
                "作者是...",
                "作者名字叫莫欣儿\n但是他正在摸鱼捏\n要不考虑赞助一下，加个速",
                self,
            ).exec()
        )
        self.setting.AboutFeedback_Button.clicked.connect(
            lambda: MessageBox(
                "反馈功能没做捏",
                "有什么事QQ群里不能说?",
                self,
            ).exec()
        )
        self.setting.AboutSponsor_Button.clicked.connect(
            lambda: MessageBox(
                "赞助功能还没做捏，我知道你很急，但你先别急",
                "赞助二维码加载失败，请重试",
                self,
            ).exec()
        )

    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.home, FIF.HOME, "主页面")
        # self.addSubInterface(self.account, FIF.ACCEPT_MEDIUM, "账号管理")
        self.addSubInterface(
            self.setting, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )
        self.navigationInterface.setExpandWidth(280)

    def initWindow(
        self,
    ):
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        # self.setMinimumSize(960, 720)
        self.resize(1280, 730)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        loop.exec()

    def ShowGetGamePathMessage(self):
        title = "找不到游戏位置"
        content = (
            """你可能是第一次使用原神Ex，或者游戏位置发生变更，请选择正确的游戏位置"""
        )
        w = MessageBox(title, content, self)
        if w.exec():
            Call.SelectGamePath()
        else:
            pass


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    # install translator
    translator = FluentTranslator()
    app.installTranslator(translator)
    w = Window()

    w.show()
    app.exec_()
