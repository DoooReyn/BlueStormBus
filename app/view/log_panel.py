#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: log_panel.py
#  Author: DoooReyn
#  Description: 日志面板
from PySide6.QtWidgets import QGroupBox, QTextBrowser, QHBoxLayout

from helper.env import gEnv
from helper.signals import gSignals


class LogUI(object):
    def __init__(self, parent: QGroupBox):
        self.parent = parent

        self.parent.setMinimumHeight(128)
        self.parent.setMaximumHeight(512)
        self.browser = QTextBrowser()

        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        self.parent.setLayout(layout)


class LogPanel(QGroupBox):
    def __init__(self, parent=None):
        super(LogPanel, self).__init__('输出', parent)

        self.ui = LogUI(self)

        self.setupSignals()

    def setupSignals(self):
        gSignals.LogDebug.connect(lambda msg: self.onAppendLog(1, msg))
        gSignals.LogInfo.connect(lambda msg: self.onAppendLog(1, msg))
        gSignals.LogWarn.connect(lambda msg: self.onAppendLog(1, msg))
        gSignals.LogError.connect(lambda msg: self.onAppendLog(1, msg))
        gSignals.LogFatal.connect(lambda msg: self.onAppendLog(1, msg))

    def onAppendLog(self, kind: int, msg: str):
        gEnv.log(f'log<{kind}>: {msg}')
        self.ui.browser.append(msg)
