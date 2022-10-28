#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: primary_controller.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget

from mvc.controller.base_controller import BaseController
from mvc.model.primary_model import PrimaryModel


class PrimaryController(BaseController):
    def __init__(self, view: QWidget, model: PrimaryModel):
        super(PrimaryController, self).__init__(view, model)

        self.model.sync()
