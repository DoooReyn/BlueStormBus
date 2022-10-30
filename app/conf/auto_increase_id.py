#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: auto_increase_id.py
#  Author: DoooReyn
#  Description:


class AutoIncreaseId:
    def __init__(self):
        self._id = 0

    def get(self):
        self._id += 1
        return self._id
