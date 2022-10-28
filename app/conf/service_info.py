# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: service_info.py
#  Author: DoooReyn
#  Description: 服务信息


class AutoIncreaseId:
    def __init__(self):
        self._id = 0

    def get(self):
        self._id += 1
        return self._id


class ServiceInfo:
    ID = AutoIncreaseId()

    def __init__(self, key: str, title: str, tooltip: str):
        self.key = key
        self.title = title
        self.tooltip = tooltip
        self.id = ServiceInfo.ID.get()

    def __str__(self):
        return f"<{self.id}> [{self.key}] {self.title}"

    def __repr__(self):
        return self.__str__()
