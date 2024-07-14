# coding:utf-8
from PyQt5.QtWidgets import QWidget
from ui.account_ui import Ui_account
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (
    QPixmap,
    QPainter,
    QPainterPath,
    QColor,
    QBrush,
    QPen,
)
from qfluentwidgets import isDarkTheme


class Account(Ui_account, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

    # def paintEvent(self, e):
    #     super().paintEvent(e)
    #     painter = QPainter(self)
    #     self.banner = QPixmap("./rescourse/background.png")
    #     painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
    #     painter.setPen(Qt.NoPen)

    #     path = QPainterPath()
    #     path.setFillRule(Qt.WindingFill)
    #     w, h, r = self.width(), self.height(), 50
    #     path.addRect(QRectF(w - 50, r, 50, 50))
    #     path.addRect(QRectF(0, h - 50, 50, 50))

    #     if not isDarkTheme():
    #         pen = QPen(QColor(163, 168, 168), 2, Qt.SolidLine)
    #         painter.setPen(pen)
    #     else:
    #         pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)
    #         painter.setPen(pen)

    #     painter.drawRoundedRect(QRectF(1, r, w, h - r), 15, 15)

    #     pixmap = self.banner.scaled(self.size(), transformMode=Qt.SmoothTransformation)
    #     path.addRoundedRect(QRectF(2, r, w, self.height() - r), 15, 15)
    #     painter.fillPath(path, QBrush(pixmap))
    #     painter.drawLine(1, h - r, 1, h)
    #     painter.drawLine(w - r, r, w, r)
