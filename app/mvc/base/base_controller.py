#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: base_controller.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import QObject, Signal

from helper import logger
from mvc.base.base_model import BaseModel


class BaseController(QObject):
    inited = Signal()

    def __init__(self, model: BaseModel):
        super(BaseController, self).__init__()

        self.model = model
        self.model.inited.connect(self.onInited)

    def sync(self):
        self.model.sync()

    def onInited(self):
        """在这里做初始化操作"""
        logger.debug(f"模型初始化: {self.model.format()}")
        # noinspection PyUnresolvedReferences
        self.inited.emit()

    def save(self):
        logger.debug(f"模型已保存: {self.model.format()}")
        self.model.save()
