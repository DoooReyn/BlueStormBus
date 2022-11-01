#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/1
#  Name: compress_file_item.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from helper import IO
from mvc.helper.compress_file_status import CompressFileStatus


class CompressFileItem(QWidget):
    def __init__(self, file_status: CompressFileStatus, parent: QWidget = None):
        super(CompressFileItem, self).__init__(parent)

        self._file_status = file_status

        self._lab_file = QLabel(self._file_status.src_at)
        self._lab_size_src = QLabel("--")
        self._lab_size_dst = QLabel("--")
        self._layout = QGridLayout()
        self._layout.addWidget(self._lab_file, 0, 0, 1, 1)
        self._layout.addWidget(self._lab_size_src, 0, 1, 1, 1)
        self._layout.addWidget(self._lab_size_dst, 0, 2, 1, 1)
        self._layout.setColumnStretch(0, 1)
        self._layout.setSpacing(20)
        self.setLayout(self._layout)

        self.updateSrcFilesize()

    @property
    def src_at(self):
        return self._file_status.src_at

    @property
    def dst_at(self):
        return self._file_status.dst_at

    @property
    def compressed(self):
        return self._file_status.compressed

    def setCompressed(self):
        self._file_status.compressed = True
        self.updateDstFilesize()

    def replaceDstAtByDir(self, dst_dir: str):
        return self._file_status.replaceDstAtByDir(dst_dir)

    def updateSrcFilesize(self):
        self._lab_size_src.setText(IO.getFileSizeInUnit(self._file_status.src_at))

    def updateDstFilesize(self):
        if self._file_status.compressed:
            self._lab_size_dst.setText(IO.getFileSizeInUnit(self._file_status.dst_at))
