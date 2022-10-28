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
from traceback import format_exception

from PySide6.QtWidgets import QApplication

from conf import AppInfo, Paths, ResMap, qInitResources, signals
from helper import IO, Gui, env, logger
from mvc.view.primary.primary_view import PrimaryView


def notify_exception(e_type, e_value, e_traceback):
    all_exception_lines = format_exception(e_type, e_value, e_traceback, chain=True)
    messages = '\n'.join(all_exception_lines)
    signals.e(messages)
    logger.error(messages)


class Application(QApplication):
    """应用"""

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        # 全局异常通知
        sys.excepthook = notify_exception

        # 初始化环境变量
        env.parse(sys.argv)

        # 初始化内部资源
        qInitResources()

        # 创建缓存目录
        IO.mkdir(Paths.appStorageAt())

        # 日志记录
        logger.run()

        # 初始化设置
        self.setApplicationName(AppInfo.APP_NAME)
        self.setApplicationDisplayName(AppInfo.APP_DISPLAY_NAME)
        self.setApplicationVersion(AppInfo.APP_VERSION)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.setStyleSheet(IO.read(ResMap.THEME_DEFAULT))

        # 加载主窗口
        PrimaryView().bringToTop()
        sys.exit(self.exec())


if __name__ == '__main__':
    Application()
