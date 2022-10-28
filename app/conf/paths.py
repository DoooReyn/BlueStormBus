#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: paths.py
#  Author: DoooReyn
#  Description:
from os.path import join
from typing import Sequence

from PySide6.QtCore import QStandardPaths

from conf import AppInfo


class Paths:

    @staticmethod
    def pictureAt():
        return QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)

    @staticmethod
    def documentAt():
        return QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

    @staticmethod
    def localCacheAt():
        """本地缓存路径"""
        return QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)

    @staticmethod
    def appStorageAt():
        """应用缓存路径"""
        return join(Paths.localCacheAt(), AppInfo.APP_NAME)

    @staticmethod
    def concat(start: str, paths: Sequence[str]):
        return join(start, *paths)
