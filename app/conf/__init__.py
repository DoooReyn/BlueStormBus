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
from .auto_increase_id import AutoIncreaseId
from .log_info import LogLevel, LogStyle
from .paths import Paths
from .res_map import ResMap
from .resources import qInitResources
from .service_info import *
from .signals import Signals

signals = Signals()

__all__ = (
    # Service
    "AllService",
    "MetaWatchDogService",
    "PngCompressorService",
    "JpgCompressorService",
    "ImageSplitterService",
    "TextureUnpackerService",
    "SpineAtlasUnpackerService",
    "LosslessUpscalerService",
    "AudioConverterService",
    "AudioCompressorService",
    "PasswordMasterService",
    "BilibiliAnimateService",
    "BilibiliDownloaderService",
    "SubtitleTranslatorService",
    "QrcodeService",
    "LANTransmitService",
    "Text2SpeechService",
    "OcrTranslatorService",
    "XinHuaZiDianService",
    "PinyinService",
    "UnsplashWallpaperService",
    "AlarmClockService",
    "ServiceInfo",
    "services",
    # Other
    "AppInfo",
    "AutoIncreaseId",
    "LogLevel",
    "LogStyle",
    "Paths",
    "ResMap",
    "qInitResources",
    "signals",
)
