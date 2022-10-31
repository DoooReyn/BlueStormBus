#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/31
#  Name: png_compressor_tab_controller.py
#  Author: DoooReyn
#  Description:

from mvc.base.base_controller import BaseController
from mvc.model.png_compressor_tab_model import PngCompressorTabModel


class PngCompressorTabController(BaseController):
    def __init__(self, model: PngCompressorTabModel):
        super(PngCompressorTabController, self).__init__(model)
        self.model = model

    def output(self):
        return self.model.output

    def setOutput(self, at: str):
        self.model.output = at

    def override(self):
        return self.model.override

    def setOverride(self, override: bool):
        self.model.override = override

    def colors(self):
        return self.model.colors

    def setColors(self, colors: int):
        self.model.colors = colors

    def speed(self):
        return self.model.speed

    def setSpeed(self, speed: int):
        self.model.speed = speed

    def dithering(self):
        return self.model.dithering

    def setDithering(self, dithering: float):
        self.model.dithering = dithering
