#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/31
#  Name: png_compressor_tab_model.py
#  Author: DoooReyn
#  Description:

from mvc.base.base_model import BaseModel


class PngCompressorTabModel(BaseModel):
    def __init__(self):
        super(PngCompressorTabModel, self).__init__()

        self.identifier = 'png_compressor'
        self._colors = 64
        self._speed = 4
        self._dithering = 0.5
        self._output = ''
        self._override = True

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, at):
        self._output = at

    @property
    def override(self):
        return self._override

    @override.setter
    def override(self, override: bool):
        self._override = override

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors: int):
        self._colors = colors

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: int):
        self._speed = speed

    @property
    def dithering(self):
        return self._dithering

    @dithering.setter
    def dithering(self, dithering: float):
        self._dithering = dithering

    def format(self):
        return dict(
            identifier=self.identifier,
            colors=self._colors,
            speed=self._speed,
            dithering=self._dithering,
            output=self._output,
            override=self._override
        )
