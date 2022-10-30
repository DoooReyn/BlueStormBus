#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_view.py
#  Author: DoooReyn
#  Description:
from os.path import isdir, isfile

from PySide6.QtWidgets import QWidget

from conf import ImageSplitterService
from helper import Gui
from mvc.base.base_tab_view import BaseTabView
from mvc.controller.image_splitter_tab_controller import ImageSplitterTabController
from mvc.model.image_splitter_tab_model import ImageSplitterTabModel
from mvc.ui.image_splitter_tab_ui import ImageSplitterTabUI


class ImageSplitterTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(ImageSplitterTabView, self).__init__(ImageSplitterService, parent)

        self._ui = ImageSplitterTabUI()
        self._ctrl = ImageSplitterTabController(ImageSplitterTabModel())
        self._ctrl.inited.connect(self.onInited)
        self._ctrl.sync()

    def canQuit(self):
        return True

    def onInited(self):
        self.setLayout(self._ui.layout)
        self._ui.edit_where.setText(self._ctrl.imageSrcAt())
        self._ui.edit_output.setText(self._ctrl.imageDstAt())
        self._ui.spin_rows.setValue(1)
        self._ui.spin_cols.setValue(1)
        self._ui.edit_where.textChanged.connect(self.onSrcChanged)
        self._ui.edit_output.textChanged.connect(self.onDstChanged)
        self._ui.btn_where.clicked.connect(self.onPickSrcAt)
        self._ui.btn_output.clicked.connect(self.onPickDstAt)
        self._ui.btn_generate.clicked.connect(self.onGenerate)

    def onPickSrcAt(self):
        wheres = Gui.pickFiles('选择图片', self._ctrl.imageSrcAt(), '图片(*.png *.jpg *.jpeg)', parent=self)
        if len(wheres) > 0 and isfile(wheres[0]):
            self._ui.edit_where.setText(wheres[0])

    def onPickDstAt(self):
        where = Gui.pickDirectory('选择图片输出位置', self._ctrl.imageDstAt(), self)
        if isdir(where):
            self._ui.edit_output.setText(where)

    def onSrcChanged(self):
        self._ctrl.setImageSrcAt(self._ui.edit_where.text())

    def onDstChanged(self):
        self._ctrl.setImageDstAt(self._ui.edit_output.text())

    def onGenerate(self):
        # TODO
        # PIL 生成
        # 允许拖拽
        pass

    def onSave(self):
        self._ctrl.save()
