#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: bse_model.py
#  Author: DoooReyn
#  Description:
from typing import Any

from PySide6.QtCore import QObject, QRect, Signal

from conf import Paths
from helper import IO


class BaseModel(QObject):
    status_inited = Signal()

    def __init__(self):
        super(BaseModel, self).__init__()
        self._data = self.template()
        self._where = Paths.concat(Paths.appStorageAt(), [self.identifier + '.json'])

    # noinspection PyMethodMayBeStatic
    # @override
    def template(self):
        """数据模板"""
        return {
            "identifier": "unknown",  # required [readonly]
            "geometry": [-1, -1, -1, -1],  # required by view
            "minium_size": [640, 480],  # required by view [readonly]
        }

    @property
    def identifier(self):
        """视图标识"""
        return self.get('identifier')

    @property
    def geometry(self):
        """视图几何信息"""
        return QRect(*self.get('geometry'))

    @geometry.setter
    def geometry(self, geometry: QRect):
        """设置视图几何信息"""
        self.set('geometry', [geometry.topLeft().x(), geometry.topLeft().y(), geometry.width(), geometry.height()])

    @property
    def miniumSize(self):
        """视图最小尺寸"""
        return self.get('minium_size')

    def isUnsetGeometry(self):
        """视图是否初始化"""
        x, y, w, h = self.get('geometry')
        return x == -1 and y == -1 and w == -1 and h == -1

    def sync(self):
        """同步存储数据"""
        data = IO.read(self._where)
        if data:
            data = IO.jsonDecode(data)
            for k, v in data.items():
                self._data[k] = v
        self.save()
        # noinspection PyUnresolvedReferences
        self.status_inited.emit()

    def save(self):
        """保存数据"""
        IO.write(self._where, IO.jsonEncode(self._data))

    def get(self, key: str):
        """获取储存数据"""
        return self._data.get(key)

    def set(self, key: str, value: Any):
        """设置储存数据"""
        self._data[key] = value
