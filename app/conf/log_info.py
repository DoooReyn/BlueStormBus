#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: log_info.py
#  Author: DoooReyn
#  Description:
from enum import Enum


class LogLevel(Enum):
    Void = 0
    Debug = 1
    Info = 2
    Warn = 3
    Error = 4


class LogStyle:
    Void = '<span style="color:#d5d5d5;">{}</span>'
    Debug = '<span style="color:#f4f4f4;">{}</span>'
    Info = '<span style="color:#2ecc71;">{}</span>'
    Warn = '<span style="color:#ffc312;">{}</span>'
    Error = '<span style="color:#ff3f34;">{}</span>'
