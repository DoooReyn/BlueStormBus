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
    def __init__(self, key: str, title: str, tooltip: str):
        global gTabId
        self.key = key
        self.title = title
        self.tooltip = tooltip
        self.id = gTabId.get()


gTabId = AutoIncreaseId()
