#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: primary_view.py
#  Author: DoooReyn
#  Description: 主窗口
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QMessageBox, QSplitter, QVBoxLayout

from conf.app_info import AppInfo
from conf.res_map import ResMap
from helper.gui import Gui
from helper.profile import Profile
from view.log_panel import LogPanel
from view.services_panel import ServicesPanel
from view.view_base import BaseView


class PrimaryProfile(Profile):
    """主视图数据存储器"""

    def template(self):
        return {
            "identifier": "primary",  # required
            "geometry": [-1, -1, -1, -1, ],  # required by view
            "minium_size": [960, 640, ],  # required by view
        }


class PrimaryUI(object):
    def __init__(self, view=None):
        self.view = view

        self.content = QWidget()
        layout = QVBoxLayout()
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(ServicesPanel())
        splitter.addWidget(LogPanel(self.view))
        splitter.setHandleWidth(10)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(7, 3)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, True)
        layout.addWidget(splitter)
        self.content.setLayout(layout)


class PrimaryView(QMainWindow, BaseView):
    def __init__(self, parent=None):
        super(PrimaryView, self).__init__(parent)

        # 初始化设置
        self.setWindowTitle(AppInfo.APP_DISPLAY_NAME)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.setProfile(PrimaryProfile(filename='primary'))

        # 设置UI
        self.ui = PrimaryUI(self)
        self.setCentralWidget(self.ui.content)

    def closeEvent(self, event):
        """拦截主窗口关闭事件"""
        msg = QMessageBox(QMessageBox.Icon.Warning,
                          '退出',
                          '关闭主窗口将停止所有服务，是否确认退出？',
                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                          self)
        code = msg.exec()
        if code == QMessageBox.StandardButton.Yes:
            event.accept()
            super(PrimaryView, self).closeEvent(event)
        elif code == QMessageBox.StandardButton.No:
            event.ignore()
