#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: primary_controller.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_view_controller import BaseViewController
from mvc.model.primary_model import PrimaryModel


class PrimaryController(BaseViewController):
    def __init__(self, model: PrimaryModel):
        super(PrimaryController, self).__init__(model)
