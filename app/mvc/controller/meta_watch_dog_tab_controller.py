#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_tab_controller.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Signal

from mvc.base.base_controller import BaseController
from mvc.model.meta_watch_dog_model import MetaWatchDogTabModel


class MetaWatchDogTabController(BaseController):
    lastProjectAtValueChanged = Signal(str)
    syncAfterValueChanged = Signal(int)

    def __init__(self, model: MetaWatchDogTabModel):
        super(MetaWatchDogTabController, self).__init__(model)
        self.model = model

        # noinspection PyUnresolvedReferences
        self.lastProjectAtValueChanged.connect(self.onLastProjectAtValueChanged)
        # noinspection PyUnresolvedReferences
        self.syncAfterValueChanged.connect(self.onSyncAfterValueChanged)

    def lastProjectAt(self):
        return self.model.lastProjectAt

    def syncAfter(self):
        return self.model.syncAfter

    def onLastProjectAtValueChanged(self, at: str):
        self.model.lastProjectAt = at

    def onSyncAfterValueChanged(self, after: int):
        self.model.syncAfter = after
