#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: base_view_controller.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import QRect

from mvc.base.base_controller import BaseController
from mvc.base.base_view_model import BaseViewModel


class BaseViewController(BaseController):
    def __init__(self, model: BaseViewModel):
        super(BaseViewController, self).__init__(model)

        self.model = model

    def syncGeometry(self, geometry: QRect):
        self.model.geometry = geometry

    def geometry(self):
        return self.model.geometry

    def miniumSize(self):
        return self.model.miniumSize
