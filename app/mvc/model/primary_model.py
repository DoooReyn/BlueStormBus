#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: primary_model.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_view_model import BaseViewModel


class PrimaryModel(BaseViewModel):
    def __init__(self):
        super(PrimaryModel, self).__init__()

        self.identifier = 'primary'
