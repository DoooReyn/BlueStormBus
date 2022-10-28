#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: base_controller.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from mvc.model.base_model import BaseModel


class BaseController(QObject):
    def __init__(self, view: QWidget, model: BaseModel):
        super(BaseController, self).__init__()

        self.view = view
        self.model = model
        self.model.status_inited.connect(self.onModelInited)

    def onModelInited(self):
        self.view.setGeometry(self.model.geometry)
        self.view.setMinimumSize(*self.model.miniumSize)

    def save(self):
        if not (self.view.isFullScreen() or self.view.isMaximized() or self.view.isMinimized()):
            # 只有正常模式下才需要保存位置数据
            self.model.geometry = self.view.geometry()
        self.model.save()
