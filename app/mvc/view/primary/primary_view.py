#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: primary_view.py
#  Author: DoooReyn
#  Description:
import time

from PySide6.QtWidgets import QMainWindow, QWidget

from conf import LogStyle, LogLevel, signals, ServiceInfo, AppInfo, ResMap
from helper import Gui, logger
from mvc.controller.primary_controller import PrimaryController
from mvc.model.primary_model import PrimaryModel
from mvc.view.base_view import BaseView
from mvc.view.primary.primary_ui import PrimaryUI
from view.tabs.meta_watch_dog_tab import MetaWatchDogTab
from view.tabs.primary_tab import PrimaryTab


class PrimaryView(QMainWindow, BaseView):
    def __init__(self, parent: QWidget = None):
        super(PrimaryView, self).__init__(parent)

        self.setWindowTitle(AppInfo.APP_DISPLAY_NAME)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.ui = PrimaryUI()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.container())
        self.ui.openTab(PrimaryTab(self), '组件列表')
        self.ui.setTabCloseBtnHidden(0)
        self.ctrl = PrimaryController(self, PrimaryModel())
        self.setupSignals()

    def setupSignals(self):
        signals.LogDebug.connect(lambda msg: self.onAppendLog(LogLevel.Debug, msg))
        signals.LogInfo.connect(lambda msg: self.onAppendLog(LogLevel.Info, msg))
        signals.LogWarn.connect(lambda msg: self.onAppendLog(LogLevel.Warn, msg))
        signals.LogError.connect(lambda msg: self.onAppendLog(LogLevel.Error, msg))
        signals.TabOpenRequested.connect(self.onTabOpenRequested)
        signals.TabCloseAllowed.connect(self.onTabCloseAllowed)

    def onTabOpenRequested(self, service: ServiceInfo):
        opened = self.ui.findTab(service.title)
        if opened == -1:
            if hasattr(self, service.key):
                widget = getattr(self, service.key)(service)
                opened = self.ui.openTab(widget, service.title)
            else:
                return signals.w(f'服务{service.key}未实现！')
        self.ui.switchTab(opened)

    def onTabCloseAllowed(self, index: int):
        if index > 0:
            self.ui.closeTab(index)

    def onAppendLog(self, kind: LogLevel, msg: str):
        self.appendFmtLog(kind, time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()))
        for sec in msg.split('\n'):
            self.appendFmtLog(kind, sec)

    def appendFmtLog(self, kind: LogLevel, msg: str):
        self.ui.appendLog(getattr(LogStyle, kind.name).format(msg))
        logger.debug(msg)

    def onClose(self):
        # TODO 关闭所有服务
        pass

    def onSave(self):
        self.ctrl.save()

    def closeEvent(self, event):
        """拦截主窗口关闭事件"""

        def ok():
            event.accept()
            super(PrimaryView, self).closeEvent(event)

        def bad():
            event.ignore()

        Gui.popup('退出', '关闭主窗口将停止所有服务，是否退出？', self, ok, bad)

    @staticmethod
    def meta_watch_dog(service):
        return MetaWatchDogTab(service)
        # print(service)
