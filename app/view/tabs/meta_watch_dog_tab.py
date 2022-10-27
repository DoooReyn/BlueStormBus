# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: meta_watch_dog_tab.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QGridLayout, QTextEdit, QPushButton, QLineEdit, QMenu

from conf.service_info import ServiceInfo
from helper.gui import Gui
from helper.profile import Profile
from helper.signals import gSignals
from view.tabs.tab_base import TabBase


class MetaWatchDogProfile(Profile):
    def template(self):
        return {
            "identifier": "primary",  # required
            "last_project_at": "",  # required
        }

    def setLastProjectAt(self, at: str):
        self.set("last_project_at", at)

    def getLastProjectAt(self):
        return self.get("last_project_at")


class MetaWatchDogTabUI(object):
    def __init__(self, view: QWidget, service: ServiceInfo):
        super(MetaWatchDogTabUI, self).__init__()

        self.view = view

        self.layout = QGridLayout()
        self.edit_help = QTextEdit(service.tooltip)
        self.edit_help.setReadOnly(True)
        self.edit_help.setStyleSheet('QTextEdit { background-color: #f0f0f0; }')
        self.edit_help.setFixedHeight(max(self.edit_help.document().size().height(), 64))
        self.edit_where = QLineEdit('')
        self.edit_where.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_where.setPlaceholderText('打开 Cocos Creator 项目')
        self.edit_where.setReadOnly(True)
        self.btn_open = QPushButton('浏览')
        self.btn_operate = QPushButton('启动服务')
        self.btn_operate.setFixedSize(96, 24)
        self.btn_operate.setStyleSheet(
            'QPushButton { border: 1px solid #34495e;  font-size:14px; color: #222222; background-color: #7bed9f; }'
            'QPushButton:checked { color: #ffffff; background-color: #ff4757; }')
        self.btn_operate.setCheckable(True)
        self.btn_operate.setChecked(False)
        self.edit_log = QTextEdit('')
        self.edit_log.setReadOnly(True)

        self.layout.addWidget(self.edit_help, 0, 0, 2, 10)
        self.layout.addWidget(self.edit_where, 2, 0, 1, 8)
        self.layout.addWidget(self.btn_open, 2, 8, 1, 1)
        self.layout.addWidget(self.btn_operate, 2, 9, 1, 1)
        self.layout.addWidget(self.edit_log, 3, 0, 7, 10)
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(9, 1)
        self.view.setLayout(self.layout)


class MetaWatchDogTab(TabBase):
    def __init__(self, service: ServiceInfo, parent=None):
        super(MetaWatchDogTab, self).__init__(service, parent)

        self.service = service
        self.profile = MetaWatchDogProfile(filename='meta_watch_dog')
        self.ui = MetaWatchDogTabUI(self, service)
        self.setupSignals()
        self.setupUi()

    # noinspection PyUnresolvedReferences
    def setupSignals(self):
        self.ui.edit_where.textChanged.connect(self.onProjectPathChanged)
        self.ui.btn_open.clicked.connect(self.onBrowserProjectPath)
        self.ui.btn_operate.clicked.connect(self.onCheckServiceState)
        self.ui.edit_where.customContextMenuRequested.connect(self.onProjectPathContextMenuRequested)
        gSignals.TabCloseRequested.connect(self.onCloseRequested)

    def setupUi(self):
        self.ui.edit_where.setText(self.profile.getLastProjectAt())

    def onProjectPathChanged(self):
        self.profile.setLastProjectAt(self.ui.edit_where.text())

    def onProjectPathContextMenuRequested(self, pos):
        pop_menu = QMenu()
        act_copy = QAction('复制', self.ui.edit_where)
        act_copy.setShortcut('Ctrl+C')
        act_copy.setEnabled(len(self.ui.edit_where.text()) > 0)
        pop_menu.addAction(act_copy)

        def copy():
            self.ui.edit_where.selectAll()
            self.ui.edit_where.copy()
            self.ui.edit_where.setCursorPosition(-1)

        # noinspection PyUnresolvedReferences
        act_copy.triggered.connect(copy)
        pop_menu.exec_(self.ui.edit_where.mapToGlobal(pos))

    def onBrowserProjectPath(self):
        where = Gui.pickDirectory('选择 Cocos Creator 项目目录', self.profile.getLastProjectAt(), self)
        if where is not None:
            self.ui.edit_where.setText(where)

    def onCheckServiceState(self):
        if self.isRunning():
            self.stop()
        else:
            self.run()

    def run(self):
        # if len(self.ui.edit_where.text()) == 0:
        #     def finished():
        #         self.ui.btn_operate.setChecked(False)
        #     return Gui.popup('警告', '请选择 Cocos Creator 项目目录', self, finished, finished)
        self.ui.btn_operate.setChecked(True)
        self.ui.btn_operate.setText('停止服务')
        super(MetaWatchDogTab, self).run()

    def stop(self):
        super(MetaWatchDogTab, self).stop()
        self.ui.btn_operate.setChecked(False)
        self.ui.btn_operate.setText('启动服务')

    def canQuit(self):
        return not self.isRunning()

    def onQuitDenied(self):
        super(MetaWatchDogTab, self).onQuitDenied()

    def onQuitAllowed(self):
        """清理工作"""
        gSignals.TabCloseRequested.disconnect(self.onCloseRequested)
        self.profile.save()
        self.stop()
        super(MetaWatchDogTab, self).onQuitAllowed()
