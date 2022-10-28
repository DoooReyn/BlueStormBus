#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: primary_model.py
#  Author: DoooReyn
#  Description:

from helper import Gui
from mvc.model.base_model import BaseModel


class PrimaryModel(BaseModel):

    def __init__(self):
        super(PrimaryModel, self).__init__()

    def template(self):
        minium_size = [960, 640]
        geometry = Gui.rectAsList(Gui.centralGeometryOfScreen(*minium_size))
        return {
            "identifier": "primary",
            "geometry": geometry,
            "minium_size": minium_size
        }
