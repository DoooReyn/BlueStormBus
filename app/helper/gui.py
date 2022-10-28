# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: gui.py
#  Author: DoooReyn
#  Description: GUI 辅助工具
from os.path import isdir
from typing import Union, Callable

from PySide6.QtCore import QUrl, QPoint, QRect
from PySide6.QtGui import QIcon, QGuiApplication, QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog

from conf import Paths, AppInfo


class Gui:
    def __init__(self):
        pass

    @staticmethod
    def app():
        return QApplication.instance()

    @staticmethod
    def clipboard():
        return QApplication.clipboard()

    @staticmethod
    def beep():
        Gui.app().beep()

    @staticmethod
    def copyText(text: str):
        Gui.clipboard().setText(text)

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
    def rectAsList(rect: QRect):
        return [
            rect.topLeft().x(),
            rect.topLeft().y(),
            rect.width(),
            rect.height()
        ]

    @staticmethod
    def openExternalUrl(url: Union[QUrl, str]):
        QDesktopServices().openUrl(url)

    @staticmethod
    def popup(title: str,
              message: str,
              parent: QWidget,
              ok: Callable = None,
              bad: Callable = None,
              icon: QMessageBox.Icon = QMessageBox.Icon.Warning):
        buttons = QMessageBox.StandardButton.Yes
        if bad is not None:
            buttons |= QMessageBox.StandardButton.No
        code = QMessageBox(icon, title, message, buttons, parent).exec()
        if code == QMessageBox.StandardButton.Yes and ok is not None:
            ok()
        elif code == QMessageBox.StandardButton.No and bad is not None:
            bad()

    @staticmethod
    def pickFiles(title: str, start: str, file_filter: str = 'Any Files(*.*)', multiple: bool = False,
                  parent: QWidget = None):
        start = start if len(start) > 0 else Paths.documentAt()
        if multiple:
            chosen = QFileDialog.getOpenFileNames(parent, title, start, file_filter)
        else:
            chosen = QFileDialog.getOpenFileName(parent, title, start, file_filter)
        if isinstance(chosen, tuple) and len(chosen) > 0:
            return chosen

    @staticmethod
    def pickDirectory(title: str, start: str, parent: QWidget):
        start = start if len(start) > 0 else Paths.documentAt()
        chosen = QFileDialog.getExistingDirectory(parent, title, start)
        if isdir(chosen):
            return chosen
