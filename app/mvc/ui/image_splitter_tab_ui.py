#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_ui.py
#  Author: DoooReyn
#  Description:
from os.path import exists, realpath, isdir

from PySide6.QtCore import Qt, QPoint, QUrl, QMimeData
from PySide6.QtGui import QDropEvent, QAction, QDragEnterEvent
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMenu, QCheckBox

from helper import Gui


class DroppableLineEdit(QLineEdit):
    def __init__(self, file_or_dir: bool, *args, **kwargs):
        super(DroppableLineEdit, self).__init__(*args, **kwargs)
        self._file_or_dir = file_or_dir
        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

    def dragEnterEvent(self, event: QDragEnterEvent):
        data: QMimeData = event.mimeData()
        where = QUrl(data.text()).toLocalFile()
        if self._file_or_dir:
            if exists(where) and where.lower().endswith(('.png', '.jpg', '.jpeg',)):
                event.setAccepted(True)
                event.acceptProposedAction()
        else:
            if exists(where) and isdir(where):
                event.setAccepted(True)
                event.acceptProposedAction()
        super(DroppableLineEdit, self).dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        where = event.mimeData().text()
        where = QUrl(where).toLocalFile()
        self.setText(realpath(where))
        event.accept()
        super(DroppableLineEdit, self).dropEvent(event)

    def copyAll(self):
        self.selectAll()
        self.copy()
        self.deselect()

    def open(self):
        where = self.text()
        if exists(where):
            Gui.openExternalUrl(QUrl.fromLocalFile(where))

    def onCustomContextMenuRequested(self, pos: QPoint):
        act_copy = QAction('复制', self)
        act_copy.setEnabled(len(self.text()) > 0)
        act_copy.triggered.connect(self.copyAll)
        act_open = QAction('打开', self)
        act_open.setEnabled(len(self.text()) > 0)
        act_open.triggered.connect(self.open)

        pop_menu = QMenu()
        pop_menu.addAction(act_copy)
        pop_menu.addAction(act_open)

        pop_menu.exec_(self.mapToGlobal(pos))


class ImageSplitterTabUI(object):
    def __init__(self):
        self.lab_where = QLabel('图像文件目录')
        self.lab_output = QLabel('图像输出目录')
        self.lab_rows = QLabel('行数')
        self.lab_cols = QLabel('列数')
        self.edit_where = DroppableLineEdit(file_or_dir=True)
        self.edit_output = DroppableLineEdit(file_or_dir=False)
        self.spin_rows = QSpinBox()
        self.spin_cols = QSpinBox()
        self.btn_where = QPushButton('..')
        self.btn_output = QPushButton('..')
        self.btn_generate = QPushButton('拆分图像')
        self.box_auto_stretch = QCheckBox('强制等分')
        self.box_delete = QCheckBox('清空输出目录')

        self.edit_where.setAcceptDrops(True)
        self.edit_output.setAcceptDrops(True)
        self.spin_rows.setMinimum(1)
        self.spin_cols.setMinimum(1)
        self.btn_generate.setMinimumHeight(36)
        self.box_auto_stretch.setToolTip('无法等分的图像会损失部分分辨率')

        self.layout = QGridLayout()
        self.layout.addWidget(self.lab_where, 0, 0, 1, 1)
        self.layout.addWidget(self.edit_where, 0, 1, 1, 2)
        self.layout.addWidget(self.btn_where, 0, 3, 1, 1)
        self.layout.addWidget(self.lab_output, 1, 0, 1, 1)
        self.layout.addWidget(self.edit_output, 1, 1, 1, 2)
        self.layout.addWidget(self.btn_output, 1, 3, 1, 1)
        self.layout.addWidget(self.lab_rows, 2, 0, 1, 1)
        self.layout.addWidget(self.spin_rows, 2, 1, 1, 1)
        self.layout.addWidget(self.lab_cols, 3, 0, 1, 1)
        self.layout.addWidget(self.spin_cols, 3, 1, 1, 1)
        self.layout.addWidget(self.box_auto_stretch, 4, 0, 1, 1)
        self.layout.addWidget(self.box_delete, 4, 1, 1, 1)
        self.layout.addWidget(self.btn_generate, 5, 0, 1, 4)
        self.layout.setColumnStretch(2, 1)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
