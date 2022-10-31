#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/31
#  Name: png_compressor_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QSlider, QSpinBox, \
    QGridLayout, QLineEdit, QListWidget, QCheckBox, QWidget


class PngCompressorTabUI(object):
    def __init__(self):
        # 1.0 选项框
        self.box_options = QFrame()

        # 1.1 颜色采样
        self.lab_colors = QLabel('颜色数量')
        self.slider_colors = QSlider(Qt.Orientation.Horizontal)
        self.spin_colors = QSpinBox()
        self.slider_colors.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider_colors.setPageStep(16)
        self.slider_colors.setMinimum(2)
        self.slider_colors.setMaximum(256)
        self.spin_colors.setMinimum(2)
        self.spin_colors.setMaximum(256)

        # 1.2 采样速度
        self.lab_speed = QLabel('采样速度')
        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.spin_speed = QSpinBox()
        self.slider_speed.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider_speed.setPageStep(1)
        self.slider_speed.setMinimum(1)
        self.slider_speed.setMaximum(11)
        self.spin_speed.setMinimum(1)
        self.spin_speed.setMaximum(11)

        # 1.3 算法平滑
        self.lab_dithered = QLabel('算法平滑')
        self.slider_dithered = QSlider(Qt.Orientation.Horizontal)
        self.spin_dithered = QSpinBox()
        self.slider_dithered.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.slider_dithered.setPageStep(1)
        self.slider_dithered.setMinimum(1)
        self.slider_dithered.setMaximum(10)
        self.spin_dithered.setMinimum(1)
        self.spin_dithered.setMaximum(10)

        # 1.4 输出目录
        self.check_override = QCheckBox('覆盖')
        self.widget_output = QWidget()
        self.lab_output = QLabel('输出目录')
        self.edit_output = QLineEdit()
        self.btn_output = QPushButton('..')

        # 1.5 布局
        self.box_options_layout = QGridLayout()
        self.box_options_layout.addWidget(self.lab_colors, 0, 0, 1, 1)
        self.box_options_layout.addWidget(self.slider_colors, 0, 1, 1, 2)
        self.box_options_layout.addWidget(self.spin_colors, 0, 3, 1, 1)
        self.box_options_layout.addWidget(self.lab_speed, 1, 0, 1, 1)
        self.box_options_layout.addWidget(self.slider_speed, 1, 1, 1, 2)
        self.box_options_layout.addWidget(self.spin_speed, 1, 3, 1, 1)
        self.box_options_layout.addWidget(self.lab_dithered, 2, 0, 1, 1)
        self.box_options_layout.addWidget(self.slider_dithered, 2, 1, 1, 2)
        self.box_options_layout.addWidget(self.spin_dithered, 2, 3, 1, 1)
        self.box_options_layout.addWidget(self.check_override, 3, 0, 1, 1)
        self.box_options_layout.addWidget(self.lab_output, 3, 1, 1, 1)
        self.box_options_layout.addWidget(self.edit_output, 3, 2, 1, 1)
        self.box_options_layout.addWidget(self.btn_output, 3, 3, 1, 1)
        self.box_options_layout.setSpacing(4)
        self.box_options.setLayout(self.box_options_layout)
        self.box_options_layout.setColumnStretch(2, 1)
        widgets = [self.slider_colors, self.slider_speed, self.slider_dithered]
        # [w.setHidden(True) for w in widgets]

        # 2.0 文件列表
        self.box_files = QGroupBox('文件列表')
        self.list_files = QListWidget()
        self.btn_add_files = QPushButton('添加文件')
        self.btn_add_dir = QPushButton('添加目录')
        self.btn_clear = QPushButton('清空')
        self.btn_start = QPushButton('压缩')

        # 2.1 布局
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

        # 4.布局
        self.layout = QGridLayout()
        self.layout.addWidget(self.box_options, 0, 0)
        self.layout.addWidget(self.box_files, 1, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
