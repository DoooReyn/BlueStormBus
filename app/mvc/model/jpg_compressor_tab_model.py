#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: jpg_compressor_tab_model.py
#  Author: DoooReyn
#  Description:


from mvc.base.base_model import BaseModel


class JpgCompressorTabModel(BaseModel):
    def __init__(self):
        super(JpgCompressorTabModel, self).__init__()

        self.identifier = 'jpg_compressor'
        self._output = ''
        self._quality = 80
        self._strip = True
        self._clean = False

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, q: int):
        self._quality = q

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, o: str):
        self._output = o

    @property
    def strip(self):
        return self._strip

    @strip.setter
    def strip(self, b: bool):
        self._strip = b

    @property
    def clean(self):
        return self._clean

    @clean.setter
    def clean(self, b: bool):
        self._clean = b

    def format(self):
        return dict(
            identifier=self.identifier,
            strip=self._strip,
            quality=self._quality,
            output=self._output,
            clean=self._clean
        )
