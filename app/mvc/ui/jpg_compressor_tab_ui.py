#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: jpg_compressor_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox, QListWidget, QGroupBox, QAbstractItemView, \
    QGridLayout, QSlider, QSpinBox, QMenu

from conf import Paths
from helper import Gui


class JpgCompressorTabUI(object):
    def __init__(self):
        self.lab_output = QLabel('输出目录')
        self.edit_output = QLineEdit('')
        self.btn_output = QPushButton('..')
        self.check_strip = QCheckBox('删除标记')
        self.check_clean = QCheckBox('清空输出目录')
        self.lab_quality = QLabel('质量')
        self.slider_quality = QSlider(Qt.Orientation.Horizontal)
        self.spin_quality = QSpinBox()
        self.box_files = QGroupBox('文件列表')
        self.list_files = QListWidget()
        self.btn_add_files = QPushButton('添加文件')
        self.btn_add_dir = QPushButton('添加目录')
        self.btn_clear = QPushButton('清空')
        self.btn_start = QPushButton('压缩')

        self.slider_quality.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider_quality.setTickInterval(10)
        self.slider_quality.setPageStep(10)
        self.slider_quality.setMinimum(0)
        self.slider_quality.setMaximum(100)
        self.spin_quality.setMinimum(0)
        self.spin_quality.setMaximum(100)
        self.edit_output.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_output.customContextMenuRequested.connect(self.onOutputContextMenuRequested)
        self.list_files.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_files.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)

        self.box_files_layout = QGridLayout()
        self.box_files_layout.addWidget(self.btn_add_files, 0, 0, 1, 1)
        self.box_files_layout.addWidget(self.btn_add_dir, 0, 1, 1, 1)
        self.box_files_layout.addWidget(self.btn_clear, 0, 2, 1, 1)
        self.box_files_layout.addWidget(self.btn_start, 0, 3, 1, 1)
        self.box_files_layout.addWidget(self.list_files, 1, 0, 1, 4)
        self.box_files_layout.setColumnStretch(3, 1)
        self.box_files_layout.setRowStretch(1, 1)
        self.box_files_layout.setSpacing(4)
        self.box_files.setLayout(self.box_files_layout)

        self.layout = QGridLayout()
        self.layout.addWidget(self.lab_output, 0, 0, 1, 1)
        self.layout.addWidget(self.edit_output, 0, 1, 1, 2)
        self.layout.addWidget(self.btn_output, 0, 3, 1, 1)
        self.layout.addWidget(self.lab_quality, 1, 0, 1, 1)
        self.layout.addWidget(self.slider_quality, 1, 1, 1, 2)
        self.layout.addWidget(self.spin_quality, 1, 3, 1, 1)
        self.layout.addWidget(self.check_strip, 2, 0, 1, 1)
        self.layout.addWidget(self.check_clean, 2, 1, 1, 1)
        self.layout.addWidget(self.box_files, 3, 0, 1, 4)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.setColumnStretch(2, 1)
        self.layout.setRowStretch(3, 1)

        self.stateful_widgets = (
            self.btn_clear,
            self.btn_start,
            self.btn_output,
            self.btn_add_dir,
            self.btn_add_files,
            self.edit_output,
            self.check_clean,
            self.check_strip,
            self.slider_quality,
            self.spin_quality,
        )

    def setStatefulWidgetsEnabled(self, enabled: bool):
        [w.setEnabled(enabled) for w in self.stateful_widgets]

    def onOutputContextMenuRequested(self, pos: QPoint):
        menu = QMenu()

        act_open = QAction('打开')
        act_open.triggered.connect(lambda: Gui.openExternalUrl(Paths.fromLocalFile(self.edit_output.text())))
        act_open.setEnabled(not not self.edit_output.text())
        menu.addAction(act_open)

        menu.exec_(self.edit_output.mapToGlobal(pos))
