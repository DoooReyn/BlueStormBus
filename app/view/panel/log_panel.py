#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: log_panel.py
#  Author: DoooReyn
#  Description:
#
#  Since: 2022/10/25
#  Name: log_panel.py
#  Author: DoooReyn
#  Description: 日志面板
import time
from enum import Enum

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QTextOption, QAction
from PySide6.QtWidgets import QGroupBox, QTextBrowser, QHBoxLayout, QMenu

from helper.env import gEnv
from helper.signals import gSignals


class LogUI(object):
    def __init__(self, parent: QGroupBox):
        self.parent = parent

        self.parent.setMinimumHeight(128)
        self.parent.setMaximumHeight(512)
        self.browser = QTextBrowser()
        self.browser.setAcceptRichText(True)
        self.browser.setOpenExternalLinks(True)
        self.browser.setWordWrapMode(QTextOption.WordWrap)
        self.browser.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        self.browser.setLineWrapColumnOrWidth(self.browser.width())
        self.browser.setReadOnly(True)
        self.browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.browser.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # noinspection PyUnresolvedReferences
        self.browser.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        self.parent.setLayout(layout)

    def onCustomContextMenuRequested(self, pos: QPoint):
        pop_menu = QMenu()
        act_copy = QAction('复制', self.browser, )
        act_copy.setShortcut('Ctrl+C')
        act_copy.setEnabled(self.browser.textCursor().hasSelection())
        act_all = QAction('全选', self.browser)
        act_all.setShortcut('Ctrl+A')
        act_all.setEnabled(not self.browser.document().isEmpty())
        act_clear = QAction('清空', self.browser)
        act_clear.setShortcut('Ctrl+K')
        act_clear.setEnabled(not self.browser.document().isEmpty())
        pop_menu.addAction(act_clear)
        pop_menu.addAction(act_copy)
        pop_menu.addAction(act_all)
        # noinspection PyUnresolvedReferences
        act_copy.triggered.connect(lambda: self.browser.copy())
        # noinspection PyUnresolvedReferences
        act_all.triggered.connect(lambda: self.browser.selectAll())
        # noinspection PyUnresolvedReferences
        act_clear.triggered.connect(lambda: self.browser.clear())
        pop_menu.exec_(self.browser.mapToGlobal(pos))


class LogLevel(Enum):
    Debug = 1
    Info = 2
    Warn = 3
    Error = 4


class LogStyle:
    Debug = '<span style="color:#636e72;">{}</span>'
    Info = '<span style="color:#2ecc71;">{}</span>'
    Warn = '<span style="color:#ffc312;">{}</span>'
    Error = '<span style="color:#ff3f34;">{}</span>'


class LogPanel(QGroupBox):

    def __init__(self, parent=None):
        super(LogPanel, self).__init__('输出', parent)

        self.ui = LogUI(self)
        self.setupSignals()

    def setupSignals(self):
        gSignals.LogDebug.connect(lambda msg: self.onAppendLog(LogLevel.Debug, msg))
        gSignals.LogInfo.connect(lambda msg: self.onAppendLog(LogLevel.Info, msg))
        gSignals.LogWarn.connect(lambda msg: self.onAppendLog(LogLevel.Warn, msg))
        gSignals.LogError.connect(lambda msg: self.onAppendLog(LogLevel.Error, msg))

    def onAppendLog(self, kind: LogLevel, msg: str):
        now = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        self.ui.browser.append(getattr(LogStyle, kind.name).format(now))
        for sec in msg.split('\n'):
            self.ui.browser.append(getattr(LogStyle, kind.name).format(sec))
