#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: base_view_model.py
#  Author: DoooReyn
#  Description:

from PySide6.QtCore import QRect

from helper import Gui
from mvc.base.base_model import BaseModel


class BaseViewModel(BaseModel):
    def __init__(self):
        super(BaseViewModel, self).__init__()

        self.identifier = 'base_view_model'
        self._minium_size = [640, 480]
        self._geometry = Gui.rectAsList(Gui.centralGeometryOfScreen(*self._minium_size))

    def format(self):
        return dict(
            identifier=self.identifier,
            geometry=self._geometry,
            minium_size=self._minium_size
        )

    @property
    def geometry(self):
        """视图几何信息"""
        return QRect(*self._geometry)

    @geometry.setter
    def geometry(self, g: QRect):
        """设置视图几何信息"""
        self._geometry = [g.topLeft().x(), g.topLeft().y(), g.width(), g.height()]

    @property
    def miniumSize(self):
        """视图最小尺寸"""
        return self._minium_size
