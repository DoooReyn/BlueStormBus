#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: primary_ui.py
#  Author: DoooReyn
#  Description:

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QGroupBox, QTextBrowser, QTabWidget, \
    QTextEdit


class PrimaryUI(object):

    def __init__(self):
        # 服务列表
        self.box_service = QGroupBox('服务')
        self.service_tabs = QTabWidget()
        self.service_tabs.setTabsClosable(True)
        self.box_service_layout = QVBoxLayout()
        self.box_service_layout.addWidget(self.service_tabs)
        self.box_service.setLayout(self.box_service_layout)

        # 控制台
        self.box_log = QGroupBox('控制台')
        self.box_log.setMinimumHeight(128)
        self.box_log.setMaximumHeight(512)
        self.edit_log = QTextEdit()
        self.edit_log.setReadOnly(True)
        self.edit_log.setAcceptRichText(True)
        self.edit_log.setWordWrapMode(QTextOption.WordWrap)
        self.edit_log.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        self.edit_log.setLineWrapColumnOrWidth(self.edit_log.width())
        self.edit_log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_log.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_log.setStyleSheet('QTextEdit { background-color: #0c2539; }')
        self.box_log_layout = QVBoxLayout()
        self.box_log_layout.addWidget(self.edit_log)
        self.box_log.setLayout(self.box_log_layout)

        # 窗口分割器
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.box_service)
        self.splitter.addWidget(self.box_log)
        self.splitter.setHandleWidth(10)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(7, 3)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)
        self.content = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.splitter)
        self.content.setLayout(self.layout)
