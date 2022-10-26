#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: signals.py
#  Author: DoooReyn
#  Description: 全局信号

from PySide6.QtCore import QObject, Signal

from conf.service_info import ServiceInfo


class Signals(QObject):
    """全局信号"""

    ViewOpen = Signal(str)
    ViewClose = Signal(str)
    ViewShow = Signal(str)
    ViewHide = Signal(str)
    ViewEnter = Signal(str)
    ViewExit = Signal(str)
    ViewMove = Signal(str)
    ViewResize = Signal(str)
    ViewFocusIn = Signal(str)
    ViewFocusOut = Signal(str)

    LogDebug = Signal(str)
    LogInfo = Signal(str)
    LogWarn = Signal(str)
    LogError = Signal(str)

    TabOpenRequested = Signal(ServiceInfo)


gSignals = Signals()
