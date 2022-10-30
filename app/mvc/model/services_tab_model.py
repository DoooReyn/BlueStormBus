#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: services_tab_model.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_model import BaseModel


class ServicesTabModel(BaseModel):
    def __init__(self):
        super(ServicesTabModel, self).__init__()

        self.identifier = 'services_tab'
        self._recently_set = set()
        self._recently = []

    @property
    def recently(self):
        return self._recently

    @recently.setter
    def recently(self, r):
        self._recently = r
        self._recently_set = set(r)

    def addRecently(self, tab: str):
        self._recently_set.add(tab)
        self._recently = list(self._recently_set)

    def format(self):
        return dict(
            identifier=self.identifier,
            recently=self._recently
        )
