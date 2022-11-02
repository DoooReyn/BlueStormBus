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

from PySide6.QtCore import QStandardPaths, QDir, QUrl

from conf import AppInfo


class Paths:

    @staticmethod
    def applicationAt(debug: bool = True):
        current = QDir.currentPath()
        current = join(current, '..') if debug else current
        return Paths.toLocalFile(current)

    @staticmethod
    def pngquantAt(debug: bool = True):
        app_at = Paths.applicationAt(debug)
        current = join(app_at, 'thirds', 'pngquant.exe')
        return Paths.toLocalFile(current)

    @staticmethod
    def jpegoptimAt(debug: bool = True):
        app_at = Paths.applicationAt(debug)
        current = join(app_at, 'thirds', 'jpegoptim.exe')
        return Paths.toLocalFile(current)

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
        return Paths.toLocalFile(join(Paths.localCacheAt(), AppInfo.APP_NAME))

    @staticmethod
    def concat(start: str, paths: Sequence[str]):
        return Paths.toLocalFile(join(start, *paths))

    @staticmethod
    def toLocalFile(filepath: str):
        return QUrl.fromLocalFile(filepath).toLocalFile()

    @staticmethod
    def fromLocalFile(filepath: str):
        return QUrl.fromLocalFile(filepath)
