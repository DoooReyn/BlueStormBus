# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: meta_watch_dog_tab.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget, QGridLayout, QTextEdit, QPushButton

from conf.service_info import ServiceInfo
from view.tabs.tab_base import TabBase


class MetaWatchDogTabUI(object):
    def __init__(self, view: QWidget, service: ServiceInfo):
        super(MetaWatchDogTabUI, self).__init__()

        self.view = view

        self.layout = QGridLayout()
        self.edit_help = QTextEdit(service.tooltip)
        self.edit_help.setReadOnly(True)
        self.edit_help.setStyleSheet('QTextEdit { background-color: #f0f0f0; }')
        self.edit_help.setFixedHeight(max(self.edit_help.document().size().height(), 64))
        self.btn_operate = QPushButton('启动服务')
        self.btn_operate.setFixedSize(96, 32)
        self.btn_operate.setStyleSheet(
            'QPushButton { border: 1px solid #34495e; color: #222222; background-color: #7bed9f;}'
            'QPushButton::checked { border: 1px solid #34495e; color: #ffffff; background-color: #ff4757;}'
        )
        self.btn_operate.setCheckable(True)
        self.btn_operate.setChecked(False)
        self.edit_log = QTextEdit('')
        self.edit_log.setReadOnly(True)

        self.layout.addWidget(self.edit_help, 0, 0, 2, 10)
        self.layout.addWidget(self.btn_operate, 2, 0, 1, 1)
        self.layout.addWidget(self.edit_log, 3, 0, 7, 10)
        self.layout.setColumnStretch(9, 1)
        self.layout.setRowStretch(9, 1)
        self.view.setLayout(self.layout)


class MetaWatchDogTab(TabBase):
    def __init__(self, service: ServiceInfo, parent=None):
        super(MetaWatchDogTab, self).__init__(parent)

        self.service = service
        self.ui = MetaWatchDogTabUI(self, service)
        self.setupSignals()

    # noinspection PyUnresolvedReferences
    def setupSignals(self):
        self.ui.btn_operate.clicked.connect(self.onCheckServiceState)

    def onCheckServiceState(self):
        if self.isRunning():
            self.stop()
        else:
            self.run()

    def run(self):
        super(MetaWatchDogTab, self).run()
        self.ui.btn_operate.setChecked(True)
        self.ui.btn_operate.setText('停止服务')

    def stop(self):
        super(MetaWatchDogTab, self).stop()
        self.ui.btn_operate.setChecked(False)
        self.ui.btn_operate.setText('启动服务')
