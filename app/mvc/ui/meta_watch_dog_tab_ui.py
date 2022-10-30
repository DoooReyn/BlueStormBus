#  -*- coding:utf-8 -*-

#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_tab_ui.py
#  Author: DoooReyn
#  Description:

#
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QGridLayout, QTextEdit, QLineEdit, QPushButton, QSpinBox, QLabel


class MetaWatchDogTabUI(object):
    def __init__(self):
        # 帮助
        self.edit_help = QTextEdit("")
        self.edit_help.setReadOnly(True)
        self.edit_help.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_help.setStyleSheet('QTextEdit { background-color: #f0f0f0; }')
        self.edit_help.setFixedHeight(max(self.edit_help.document().size().height(), 64))

        # 目录选择框
        self.edit_where = QLineEdit('')
        self.edit_where.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_where.setPlaceholderText('打开 Cocos Creator 项目')
        self.edit_where.setReadOnly(True)
        self.edit_where.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 浏览按钮
        self.btn_open = QPushButton('浏览')

        # 同步周期
        self.lab_sync = QLabel('同步周期(秒)')
        self.spin_sync = QSpinBox()
        self.spin_sync.setMinimum(1)
        self.spin_sync.setMaximum(3600)

        # 手动同步按钮
        self.btn_sync = QPushButton('手动同步')
        self.btn_sync.setFixedSize(96, 24)

        # 服务操作按钮
        self.btn_operate = QPushButton('启动服务')
        self.btn_operate.setFixedSize(96, 24)
        self.btn_operate.setStyleSheet(
            'QPushButton { border: 1px solid #34495e;  font-size:14px; color: #222222; background-color: #7bed9f; }'
            'QPushButton:checked { color: #ffffff; background-color: #ff4757; }')
        self.btn_operate.setCheckable(True)
        self.btn_operate.setChecked(False)

        # 日志输出
        self.edit_log = QTextEdit('')
        self.edit_log.setReadOnly(True)
        self.edit_log.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # 布局
        self.layout = QGridLayout()
        self.layout.addWidget(self.edit_help, 0, 0, 2, 10)
        self.layout.addWidget(self.edit_where, 2, 0, 1, 5)
        self.layout.addWidget(self.btn_open, 2, 5, 1, 1)
        self.layout.addWidget(self.lab_sync, 2, 6, 1, 1)
        self.layout.addWidget(self.spin_sync, 2, 7, 1, 1)
        self.layout.addWidget(self.btn_sync, 2, 8, 1, 1)
        self.layout.addWidget(self.btn_operate, 2, 9, 1, 1)
        self.layout.addWidget(self.edit_log, 3, 0, 7, 10)
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(4, 1)

    def appendLog(self, log: str):
        self.edit_log.append(log)
        self.edit_log.moveCursor(QTextCursor.MoveOperation.End)

    def clearLog(self):
        self.edit_log.clear()
