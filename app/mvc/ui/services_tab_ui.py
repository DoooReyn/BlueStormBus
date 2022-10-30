#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: primary_tab_ui.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from helper import FlowLayout


class ServicesTabUI(object):
    def __init__(self):
        self.content = QWidget()
        self.layout_flow = FlowLayout()
        self.layout_flow.setSpacing(8)
        self.content.setLayout(self.layout_flow)
        self.layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
