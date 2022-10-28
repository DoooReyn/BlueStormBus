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
    Debug = 1
    Info = 2
    Warn = 3
    Error = 4


class LogStyle:
    Debug = '<span style="color:#636e72;">{}</span>'
    Info = '<span style="color:#2ecc71;">{}</span>'
    Warn = '<span style="color:#ffc312;">{}</span>'
    Error = '<span style="color:#ff3f34;">{}</span>'
