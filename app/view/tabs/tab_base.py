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

from conf.service_info import ServiceInfo
from helper.gui import Gui
from helper.signals import gSignals


class TabBase(QWidget):
    def __init__(self, service: ServiceInfo, parent=None):
        super(TabBase, self).__init__(parent)
        self.service = service
        self._running = False
        self._quit_tab = -1

    @abstractmethod
    def run(self):
        self._running = True

    @abstractmethod
    def stop(self):
        self._running = False

    def isRunning(self):
        return self._running

    def onCloseRequested(self, index: int, title: str):
        if self.service.title == title:
            self._quit_tab = index
            self.quit()

    def quit(self):
        if self.isRunning():
            if self.canQuit():
                self.onQuitAllowed()
            else:
                self.onQuitDenied()
        else:
            self.onQuitAllowed()

    # noinspection PyMethodMayBeStatic
    def canQuit(self):
        return False

    def onQuitAllowed(self):
        gSignals.TabCloseAllowed.emit(self._quit_tab)

    def onQuitDenied(self):
        def bad():
            self._quit_tab = -1
        Gui.popup('用户请求关闭服务', '服务运行中，是否停止并退出？', self, lambda: self.onQuitAllowed(), bad)
