# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: application.py
#  Author: DoooReyn
#  Description: 应用入口

import sys
import traceback

from PySide6.QtWidgets import QApplication

from conf.app_info import AppInfo
from conf.res_map import ResMap
from conf.resources import qInitResources
from helper.env import gEnv
from helper.gui import Gui
from helper.io import io
from helper.signals import gSignals
from view.primary_view import PrimaryView


def notify_exception(e_type, e_value, e_traceback):
    all_exception_lines = traceback.format_exception(e_type, e_value, e_traceback, chain=True)
    messages = '\n'.join(all_exception_lines)
    gSignals.e(messages)


class Application(QApplication):
    """应用"""

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        sys.excepthook = notify_exception

        # 初始化环境变量
        gEnv.parse(sys.argv)

        # 初始化内部资源
        qInitResources()

        # 初始化设置
        self.setApplicationName(AppInfo.APP_NAME)
        self.setApplicationDisplayName(AppInfo.APP_DISPLAY_NAME)
        self.setApplicationVersion(AppInfo.APP_VERSION)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.setStyleSheet(io.read(ResMap.THEME_DEFAULT))

        # 加载主窗口
        self.win = PrimaryView()

    def start(self):
        """启动应用"""
        self.win.show()
        self.win.activateWindow()
        self.win.raise_()
        sys.exit(self.exec())


if __name__ == '__main__':
    Application().start()
