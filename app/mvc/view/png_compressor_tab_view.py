#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/31
#  Name: png_compressor_tab_view.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget

from conf import PngCompressorService
from mvc.base.base_tab_view import BaseTabView
from mvc.controller.png_compressor_tab_controller import PngCompressorTabController
from mvc.model.png_compressor_tab_model import PngCompressorTabModel
from mvc.ui.png_compressor_tab_ui import PngCompressorTabUI


class PngCompressorTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(PngCompressorTabView, self).__init__(PngCompressorService, parent)

        self._ui = PngCompressorTabUI()
        self._ctrl = PngCompressorTabController(PngCompressorTabModel())
        self._ctrl.inited.connect(self.onInited)
        self._ctrl.sync()

    def onInited(self):
        self.setLayout(self._ui.layout)
        self._ui.slider_colors.setValue(self._ctrl.colors())
        self._ui.spin_colors.setValue(self._ctrl.colors())
        self._ui.slider_speed.setValue(self._ctrl.speed())
        self._ui.spin_speed.setValue(self._ctrl.speed())
        self._ui.slider_dithered.setValue(self._ctrl.dithering())
        self._ui.slider_dithered.setValue(self._ctrl.dithering())
        self._ui.check_override.setChecked(self._ctrl.override())
        self._ui.edit_output.setEnabled(not self._ctrl.override())
        self._ui.btn_output.setEnabled(not self._ctrl.override())
        self._ui.slider_colors.valueChanged.connect(self.onColorsValueChanged1)
        self._ui.spin_colors.valueChanged.connect(self.onColorsValueChanged2)
        self._ui.slider_speed.valueChanged.connect(self.onSpeedValueChanged1)
        self._ui.spin_speed.valueChanged.connect(self.onSpeedValueChanged2)
        self._ui.slider_dithered.valueChanged.connect(self.onDitheringValueChanged1)
        self._ui.spin_dithered.valueChanged.connect(self.onDitheringValueChanged2)
        self._ui.check_override.stateChanged.connect(self.onOverrideStateChanged)

    def onColorsValueChanged1(self):
        value = self._ui.slider_colors.value()
        self._ui.spin_colors.setValue(value)
        self._ctrl.setColors(value)

    def onColorsValueChanged2(self):
        value = self._ui.spin_colors.value()
        self._ui.slider_colors.setValue(value)
        self._ctrl.setColors(value)

    def onSpeedValueChanged1(self):
        value = self._ui.slider_speed.value()
        self._ui.spin_speed.setValue(value)
        self._ctrl.setSpeed(value)

    def onSpeedValueChanged2(self):
        value = self._ui.spin_speed.value()
        self._ui.slider_speed.setValue(value)
        self._ctrl.setSpeed(value)

    def onDitheringValueChanged1(self):
        value = self._ui.slider_dithered.value()
        self._ui.spin_dithered.setValue(value)
        self._ctrl.setDithering(value)

    def onDitheringValueChanged2(self):
        value = self._ui.spin_dithered.value()
        self._ui.slider_dithered.setValue(value)
        self._ctrl.setDithering(value)

    def onOverrideStateChanged(self):
        checked = self._ui.check_override.isChecked()
        self._ui.edit_output.setEnabled(not checked)
        self._ui.btn_output.setEnabled(not checked)
        self._ctrl.setOverride(checked)

    def canQuit(self):
        return not self.running

    def onSave(self):
        self._ctrl.save()
        super(PngCompressorTabView, self).onSave()

    def run(self):
        # TODO
        super(PngCompressorTabView, self).run()

    def stop(self):
        # TODO
        super(PngCompressorTabView, self).stop()
