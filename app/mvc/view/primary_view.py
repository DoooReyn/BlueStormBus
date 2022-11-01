#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: primary_view.py
#  Author: DoooReyn
#  Description:
from time import strftime, localtime

from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QMainWindow, QMenu, QTabBar

from conf import AppInfo, ResMap, LogLevel, LogStyle, signals, ServiceInfo, AllService
from helper import Gui, logger
from mvc.base.base_view import BaseView
from mvc.controller.primary_controller import PrimaryController
from mvc.model.primary_model import PrimaryModel
from mvc.ui.primary_ui import PrimaryUI
from mvc.view.services_tab_view import ServicesTabView


class PrimaryView(QMainWindow, BaseView):
    def __init__(self, parent: QWidget = None):
        super(PrimaryView, self).__init__(parent)

        self._ui = PrimaryUI()
        self._ctrl = PrimaryController(PrimaryModel())
        self._ctrl.inited.connect(self.onInited)
        self._ctrl.sync()

    def onInited(self):
        self.setWindowTitle(AppInfo.APP_DISPLAY_NAME)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.setCentralWidget(self._ui.content)
        self.setMinimumSize(*self._ctrl.miniumSize())
        self.setGeometry(self._ctrl.geometry())
        self._ui.service_tabs.tabCloseRequested.connect(self.onTabCloseRequested)
        self._ui.edit_log.customContextMenuRequested.connect(self.onLogContextMenuRequested)
        signals.debug.connect(lambda msg: self.onAppendLog(LogLevel.Debug, msg))
        signals.info.connect(lambda msg: self.onAppendLog(LogLevel.Info, msg))
        signals.warn.connect(lambda msg: self.onAppendLog(LogLevel.Warn, msg))
        signals.error.connect(lambda msg: self.onAppendLog(LogLevel.Error, msg))
        signals.tab_open_requested.connect(self.onTabOpenRequested)
        signals.tab_close_allowed.connect(self.onTabCloseAllowed)
        signals.tab_added_requested.connect(self.onTabAddedRequested)

        self.openTab(ServicesTabView(), AllService.title)
        self.setTabCloseBtnHidden(0)

    def onLogContextMenuRequested(self, pos: QPoint):
        pop_menu = QMenu()
        act_copy = QAction('复制', self._ui.edit_log, )
        act_all = QAction('全选', self._ui.edit_log)
        act_clear = QAction('清空', self._ui.edit_log)
        act_copy.setShortcut('Ctrl+C')
        act_all.setShortcut('Ctrl+A')
        act_clear.setShortcut('Ctrl+K')
        act_copy.setEnabled(self._ui.edit_log.textCursor().hasSelection())
        act_all.setEnabled(not self._ui.edit_log.document().isEmpty())
        act_clear.setEnabled(not self._ui.edit_log.document().isEmpty())
        act_copy.triggered.connect(lambda: self._ui.edit_log.copy())
        act_all.triggered.connect(lambda: self._ui.edit_log.selectAll())
        act_clear.triggered.connect(lambda: self._ui.edit_log.clear())
        pop_menu.addAction(act_clear)
        pop_menu.addAction(act_copy)
        pop_menu.addAction(act_all)
        pop_menu.exec_(self._ui.edit_log.mapToGlobal(pos))

    def onTabCloseRequested(self, index: int):
        if index > 0:
            w = self._ui.service_tabs.widget(index)
            if hasattr(w, 'quitRequested'):
                getattr(w, 'quitRequested').emit()
        else:
            Gui.app().beep()

    def onTabOpenRequested(self, service: ServiceInfo):
        opened = self.findTab(service.id)
        if opened == -1:
            signals.tab_open_allowed.emit(service)
        self.switchTab(opened)

    def onTabCloseAllowed(self, index: int):
        if index > 0:
            self.closeTab(index)

    def onTabAddedRequested(self, widget: QWidget, title: str):
        index = self.openTab(widget, title)
        if hasattr(widget, 'quitAllowed'):
            getattr(widget, 'quitAllowed').connect(lambda: self.onTabCloseAllowed(index))

    def onAppendLog(self, kind: LogLevel, msg: str):
        self.appendFmtLog(LogLevel.Void, strftime("[%Y-%m-%d %H:%M:%S]", localtime()))
        for sec in msg.split('\n'):
            self.appendFmtLog(kind, sec)

    def onSave(self):
        if not (self.isFullScreen() or self.isMinimized() or self.isFullScreen()):
            self._ctrl.syncGeometry(self.geometry())
        self._ctrl.save()
        super(PrimaryView, self).onSave()

    def onClose(self):
        signals.tab_force_quit.emit()
        super(PrimaryView, self).onClose()

    def closeEvent(self, event):
        """拦截主窗口关闭事件"""

        def ok():
            event.accept()
            super(PrimaryView, self).closeEvent(event)

        def bad():
            event.ignore()

        Gui.popup('退出', '关闭主窗口将停止所有服务，是否退出？', self, ok, bad)

    def appendLog(self, msg: str):
        self._ui.edit_log.append(msg)

    def appendFmtLog(self, kind: LogLevel, msg: str):
        self.appendLog(getattr(LogStyle, kind.name).format(msg))
        logger.debug(msg)

    def setTabCloseBtnHidden(self, index: int):
        self._ui.service_tabs.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)

    def findTab(self, identifier: str):
        index = -1
        for i in range(self._ui.service_tabs.count()):
            if self._ui.service_tabs.widget(i).objectName() == identifier:
                index = i
                break
        return index

    def openTab(self, widget: QWidget, title: str):
        index = self._ui.service_tabs.addTab(widget, title)
        self.switchTab(index)
        return index

    def closeTab(self, index: int):
        self._ui.service_tabs.removeTab(index)

    def switchTab(self, index: int):
        self._ui.service_tabs.setCurrentIndex(index)

    def currentTab(self):
        return self._ui.service_tabs.currentIndex()

    def tabTitle(self, index: int):
        return self._ui.service_tabs.tabText(index)
