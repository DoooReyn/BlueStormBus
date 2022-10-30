#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: base_model.py
#  Author: DoooReyn
#  Description:
from abc import abstractmethod

from PySide6.QtCore import QObject, Signal

from conf import Paths
from helper import IO


class BaseModel(QObject):
    inited = Signal()

    def __init__(self):
        super(BaseModel, self).__init__()
        self._identifier = "base_model_identifier"

    @abstractmethod
    def format(self):
        return dict(identifier=self._identifier, )

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, mid: str):
        self._identifier = mid

    def where(self):
        return Paths.concat(Paths.appStorageAt(), [self._identifier + '.json'])

    def sync(self):
        """同步存储数据"""
        data = IO.read(self.where())
        if data:
            data = IO.jsonDecode(data)
            for k, v in data.items():
                k = f"_{k}"
                if getattr(self, k, None) is not None:
                    setattr(self, k, v)
        self.save()
        # noinspection PyUnresolvedReferences
        self.inited.emit()

    def save(self):
        """保存数据"""
        IO.write(self.where(), IO.jsonEncode(self.format()))
