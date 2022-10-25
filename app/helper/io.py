#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: io.py
#  Author: DoooReyn
#  Description: 文件系统IO操作

from json import loads, dumps, JSONDecodeError
from os import makedirs
from os.path import join, exists, isfile
from typing import List, Union, Dict, Sequence

from PySide6.QtCore import QStandardPaths, QIODevice, QFile

from conf.app_info import AppInfo
from helper.env import gEnv


class IO:
    """文件系统IO操作"""

    def __init__(self):
        self.mkdir(self.appStorageAt())

    @staticmethod
    def localCacheAt():
        """本地缓存路径"""
        return QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)

    @staticmethod
    def appStorageAt():
        """应用缓存路径"""
        return join(IO.localCacheAt(), AppInfo.APP_NAME)

    @staticmethod
    def joinPaths(start: str, paths: Sequence[str]):
        return join(start, *paths)

    @staticmethod
    def mkdir(directory: str):
        """创建目录"""
        makedirs(directory, exist_ok=True)

    @staticmethod
    def read(filepath: str, encoding='utf-8'):
        """向文件读取数据"""
        if exists(filepath) and isfile(filepath):
            file_handle = QFile(filepath)
            if file_handle.open(QIODevice.ReadOnly):
                return file_handle.readAll().data().decode(encoding=encoding)

    @staticmethod
    def write(where: str, content: str, encoding='utf-8'):
        """向文件写入数据"""
        with open(where, 'w', encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def jsonDecode(content: str):
        """json解码"""
        try:
            return loads(content)
        except (JSONDecodeError, TypeError) as e:
            gEnv.log(f'解析Json失败: {e.msg}')

    @staticmethod
    def jsonEncode(content: Union[Dict, List]):
        """json编码"""
        return dumps(content, ensure_ascii=False, indent=2)


io = IO()
