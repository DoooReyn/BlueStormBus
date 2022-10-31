#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_view.py
#  Author: DoooReyn
#  Description:
from os import makedirs
from os.path import isdir, isfile, splitext, join, basename
from shutil import rmtree

from PIL import Image
from PySide6.QtCore import QUrl
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
        where = self._ui.edit_where.text()
        output = self._ui.edit_output.text()
        auto_deleted = self._ui.box_delete.isChecked()
        auto_stretch = self._ui.box_auto_stretch.isChecked()

        if not isfile(where):
            return Gui.popup('提示', '请确认图像文件目录', self)

        if not isdir(output):
            return Gui.popup('提示', '请确认图像输出目录', self)

        rows = self._ui.spin_rows.value()
        cols = self._ui.spin_cols.value()
        if rows == 1 and cols == 1:
            return Gui.popup('提示', '1行1列视为无需分割', self)

        if auto_deleted:
            rmtree(output, ignore_errors=True)
            makedirs(output, exist_ok=True)

        im = Image.open(where)
        im_width, im_height = im.size
        row_width = int(im_width / cols)
        row_height = int(im_height / rows)
        n = 0
        for i in range(0, rows):
            for j in range(0, cols):
                x1 = j * row_width
                y1 = i * row_height
                x2 = (j + 1) * row_width if (auto_stretch or j < cols - 1) else im_width
                y2 = (i + 1) * row_height if (auto_stretch or i < rows - 1) else im_height
                box = (x1, y1, x2, y2)
                dst_im = im.crop(box)
                name, ext = splitext(basename(where))
                dst_path = join(output, f"{name}_{n}{ext}")
                dst_im.save(dst_path)
                dst_im.close()
                n += 1
        im.close()
        Gui.popup('提示',
                  '图像分割完成，是否打开输出目录？',
                  self,
                  lambda: Gui.openExternalUrl(QUrl.fromLocalFile(output)),
                  lambda: None)

    def onSave(self):
        self._ctrl.save()
