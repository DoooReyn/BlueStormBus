# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: signals.py
#  Author: DoooReyn
#  Description: 全局信号

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from conf.service_info import ServiceInfo


class Signals(QObject):
    """全局信号"""

    view_open = Signal(str)
    view_close = Signal(str)
    view_show = Signal(str)
    view_hide = Signal(str)
    view_enter = Signal(str)
    view_exit = Signal(str)
    view_move = Signal(str)
    view_resize = Signal(str)
    view_focus_in = Signal(str)
    view_focus_out = Signal(str)

    debug = Signal(str)
    info = Signal(str)
    warn = Signal(str)
    error = Signal(str)

    tab_open_requested = Signal(ServiceInfo)
    tab_open_allowed = Signal(ServiceInfo)
    tab_open_denied = Signal(ServiceInfo)
    tab_added_requested = Signal(QWidget, str)
    tab_close_allowed = Signal(int)
    tab_close_denied = Signal(int)

    tab_force_quit = Signal()
    meta_info_changed = Signal(str)

    def d(self, msg: str):
        # noinspection PyUnresolvedReferences
        self.debug.emit(msg)

    def i(self, msg: str):
        # noinspection PyUnresolvedReferences
        self.info.emit(msg)

    def w(self, msg: str):
        # noinspection PyUnresolvedReferences
        self.warn.emit(msg)

    def e(self, msg: str):
        # noinspection PyUnresolvedReferences
        self.error.emit(msg)
