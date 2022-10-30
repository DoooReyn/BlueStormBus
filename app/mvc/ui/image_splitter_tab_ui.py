#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: image_splitter_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox


class ImageSplitterTabUI(object):
    def __init__(self):
        self.lab_where = QLabel('图像文件路径')
        self.lab_output = QLabel('图像输出路径')
        self.lab_rows = QLabel('行数')
        self.lab_cols = QLabel('列数')
        self.edit_where = QLineEdit()
        self.edit_output = QLineEdit()
        self.spin_rows = QSpinBox()
        self.spin_cols = QSpinBox()
        self.btn_where = QPushButton('..')
        self.btn_output = QPushButton('..')
        self.btn_generate = QPushButton('拆分图像')

        self.edit_where.setAcceptDrops(True)
        self.edit_output.setAcceptDrops(True)
        self.spin_rows.setMinimum(1)
        self.spin_cols.setMinimum(1)
        self.btn_generate.setMinimumHeight(36)

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
        self.layout.addWidget(self.btn_generate, 4, 0, 1, 4)
        self.layout.setColumnStretch(2, 1)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
