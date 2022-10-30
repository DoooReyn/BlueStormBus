#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: __init__.py
#  Author: DoooReyn
#  Description:

from .app_info import AppInfo
from .log_info import LogLevel, LogStyle
from .paths import Paths
from .res_map import ResMap
from .resources import qInitResources
from .service_info import (
    ServiceInfo,
    AllService,
    MetaWatchDogService,
    PngCompressorService,
    JpgCompressorService,
    ImageSplitterService
)
from .signals import Signals

signals = Signals()
services = (
    MetaWatchDogService,
    PngCompressorService,
    JpgCompressorService,
    ImageSplitterService,
)

__all__ = (
    AllService,
    AppInfo,
    LogLevel,
    LogStyle,
    Paths,
    ResMap,
    ServiceInfo,
    qInitResources,
    services,
    signals,
)
