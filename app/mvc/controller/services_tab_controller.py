#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: services_tab_controller.py
#  Author: DoooReyn
#  Description:
from mvc.base.base_controller import BaseController
from mvc.model.services_tab_model import ServicesTabModel


class ServicesTabController(BaseController):
    def __init__(self, model: ServicesTabModel):
        super(ServicesTabController, self).__init__(model)
