#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: gui.py
#  Author: DoooReyn
#  Description: GUI 辅助工具

from typing import Union

from PySide6.QtCore import QUrl, QPoint
from PySide6.QtGui import QIcon, QGuiApplication, QDesktopServices

from conf.app_info import AppInfo


class Gui:
    @staticmethod
    def icon(path: str):
        return QIcon(path)

    @staticmethod
    def centralPosOfScreen():
        return QGuiApplication.primaryScreen().availableGeometry().center()

    @staticmethod
    def centralGeometryOfScreen(width: int = None, height: int = None):
        width = width or AppInfo.WIN_MIN_SIZE[0]
        height = height or AppInfo.WIN_MIN_SIZE[1]
        center = Gui.centralPosOfScreen()
        rect = QGuiApplication.primaryScreen().availableGeometry()
        rect.setTopLeft(QPoint(center.x() - width // 2, center.y() - height // 2))
        rect.setWidth(width)
        rect.setHeight(height)
        return rect

    @staticmethod
    def openExternalUrl(url: Union[QUrl, str]):
        QDesktopServices().openUrl(url)
