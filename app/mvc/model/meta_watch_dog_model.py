#  -*- coding:utf-8 -*-
from PySide6.QtCore import Signal

from mvc.base.base_model import BaseModel


#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_model.py
#  Author: DoooReyn
#  Description:

#
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_model.py
#  Author: DoooReyn
#  Description:

class MetaWatchDogTabModel(BaseModel):
    def __init__(self):
        super(MetaWatchDogTabModel, self).__init__()

        self.identifier = 'meta_watch_dog'
        self._last_project_at = ''
        self._sync_after = 60

    @property
    def lastProjectAt(self):
        return self._last_project_at

    @lastProjectAt.setter
    def lastProjectAt(self, at: str):
        self._last_project_at = at

    @property
    def syncAfter(self):
        return self._sync_after

    @syncAfter.setter
    def syncAfter(self, after: int):
        self._sync_after = after

    def format(self):
        return dict(
            identifier=self.identifier,
            last_project_at=self._last_project_at,
            sync_after=self._sync_after
        )
