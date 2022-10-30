#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: base_tab_view.py
#  Author: DoooReyn
#  Description:
from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from conf import ServiceInfo, signals
from helper import Gui
from mvc.base.base_view import BaseView


class BaseTabView(BaseView):
    quitRequested = Signal()
    quitAllowed = Signal()

    def __init__(self, service: ServiceInfo, parent: QWidget = None):
        super(BaseTabView, self).__init__(parent)

        self.service = service
        self._running = False
        self.setObjectName(service.id)
        # noinspection PyUnresolvedReferences
        self.quitRequested.connect(self.onQuitRequested)
        signals.tab_force_quit.connect(self.onClose)

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running: bool):
        self._running = running

    @abstractmethod
    def canQuit(self):
        """是否可以退出，在此处指明退出条件"""
        return False

    def run(self):
        self.running = True

    def stop(self):
        self.running = False

    def cleanupSignals(self):
        signals.tab_force_quit.disconnect(self.onClose)

    def onClose(self):
        self.stop()
        self.cleanupSignals()
        self.onSave()
        super(BaseTabView, self).onClose()

    def onQuitRequested(self):
        if self.running and (not self.canQuit()):
            self.onQuitDenied()
        else:
            self.onQuitAllowed()

    def onQuitAllowed(self):
        # noinspection PyUnresolvedReferences
        self.quitAllowed.emit()

    def onQuitDenied(self):
        Gui.popup('关闭服务', '服务运行中，是否停止并退出？', self, self.onQuitAllowed, lambda: None)
