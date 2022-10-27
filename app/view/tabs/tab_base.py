# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: tab_base.py
#  Author: DoooReyn
#  Description: 标签页基类
from abc import abstractmethod

from PySide6.QtWidgets import QWidget


class TabBase(QWidget):
    def __init__(self, parent=None):
        super(TabBase, self).__init__(parent)
        self._running = False

    @abstractmethod
    def run(self):
        self._running = True

    @abstractmethod
    def stop(self):
        self._running = False

    def isRunning(self):
        return self._running

    def closeEvent(self, event):
        if self.isRunning():
            event.ignore()
        else:
            event.accept()
            super(TabBase, self).closeEvent(event)
