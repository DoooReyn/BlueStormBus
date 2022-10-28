#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: primary_ui.py
#  Author: DoooReyn
#  Description:

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QTextOption, QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QGroupBox, QTextBrowser, QMenu, QTabWidget, \
    QTabBar

from conf import signals
from helper import Gui


class PrimaryUI(object):
    def __init__(self):
        # 服务列表
        self._box_service = QGroupBox('服务组件')
        self._service_tabs = QTabWidget()
        self._service_tabs.setTabsClosable(True)
        self._box_service_layout = QVBoxLayout()
        self._box_service_layout.addWidget(self._service_tabs)
        self._box_service.setLayout(self._box_service_layout)

        # 控制台
        self._box_log = QGroupBox('控制台')
        self._box_log.setMinimumHeight(128)
        self._box_log.setMaximumHeight(512)
        self._browser_log = QTextBrowser()
        self._browser_log.setReadOnly(True)
        self._browser_log.setAcceptRichText(True)
        self._browser_log.setOpenExternalLinks(True)
        self._browser_log.setWordWrapMode(QTextOption.WordWrap)
        self._browser_log.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        self._browser_log.setLineWrapColumnOrWidth(self._browser_log.width())
        self._browser_log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._browser_log.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._browser_log.customContextMenuRequested.connect(self.onLogContextMenuRequested)
        self._box_log_layout = QVBoxLayout()
        self._box_log_layout.addWidget(self._browser_log)
        self._box_log.setLayout(self._box_log_layout)

        # 窗口分割器
        self._splitter = QSplitter(Qt.Orientation.Vertical)
        self._splitter.addWidget(self._box_service)
        self._splitter.addWidget(self._box_log)
        self._splitter.setHandleWidth(10)
        self._splitter.setStretchFactor(0, 7)
        self._splitter.setStretchFactor(7, 3)
        self._splitter.setCollapsible(0, False)
        self._splitter.setCollapsible(1, True)
        self._content = QWidget()
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._splitter)
        self._content.setLayout(self._layout)

    def container(self):
        return self._content

    def setupUi(self, parent: QWidget):
        self._service_tabs.tabCloseRequested.connect(self.onTabCloseRequested)

    def onTabCloseRequested(self, index: int):
        if index > 0:
            signals.TabCloseRequested.emit(index, self.tabTitle(index))
        else:
            Gui.app().beep()

    def setTabCloseBtnHidden(self, index: int):
        self._service_tabs.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)

    def findTab(self, title: str):
        index = -1
        for i in range(self._service_tabs.count()):
            if self._service_tabs.tabText(i) == title:
                index = i
                break
        return index

    def openTab(self, widget: QWidget, title: str):
        return self._service_tabs.addTab(widget, title)

    def closeTab(self, index: int):
        self._service_tabs.removeTab(index)

    def switchTab(self, index: int):
        self._service_tabs.setCurrentIndex(index)

    def currentTab(self):
        return self._service_tabs.currentIndex()

    def tabTitle(self, index: int):
        return self._service_tabs.tabText(index)

    def appendLog(self, msg: str):
        self._browser_log.append(msg)

    def onLogContextMenuRequested(self, pos: QPoint):
        pop_menu = QMenu()
        act_copy = QAction('复制', self._browser_log, )
        act_all = QAction('全选', self._browser_log)
        act_clear = QAction('清空', self._browser_log)
        act_copy.setShortcut('Ctrl+C')
        act_all.setShortcut('Ctrl+A')
        act_clear.setShortcut('Ctrl+K')
        act_copy.setEnabled(self._browser_log.textCursor().hasSelection())
        act_all.setEnabled(not self._browser_log.document().isEmpty())
        act_clear.setEnabled(not self._browser_log.document().isEmpty())
        act_copy.triggered.connect(lambda: self._browser_log.copy())
        act_all.triggered.connect(lambda: self._browser_log.selectAll())
        act_clear.triggered.connect(lambda: self._browser_log.clear())
        pop_menu.addAction(act_clear)
        pop_menu.addAction(act_copy)
        pop_menu.addAction(act_all)
        pop_menu.exec_(self._browser_log.mapToGlobal(pos))
