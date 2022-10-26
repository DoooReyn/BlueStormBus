#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: primary_tab.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QScrollArea

from conf.service_info import ServiceInfo
from helper.flow_layout import FlowLayout
from helper.signals import gSignals


class PrimaryTabUI(object):
    def __init__(self, view: QWidget):
        self.view = view

        self.content = QWidget()
        self.layout_content = FlowLayout()
        self.layout_content.setSpacing(8)
        self.content.setLayout(self.layout_content)

        self.layout_main = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.content)
        self.scroll_area.setWidgetResizable(True)
        self.layout_main.addWidget(self.scroll_area)
        self.view.setLayout(self.layout_main)


class PrimaryTab(QWidget):
    def __init__(self, parent=None):
        super(PrimaryTab, self).__init__(parent)

        self.ui = PrimaryTabUI(self)

        self.appendService(ServiceInfo('meta_watch_dog', 'Meta Watch Dog', 'Cocos Creator Meta 文件监控 <OK>'))
        self.appendService(ServiceInfo('png_compressor', 'PNG Compressor', 'PNG 批量压缩 <Progress>'))
        self.appendService(ServiceInfo('jpg_compressor', 'JPG Compressor', 'JPG 批量压缩 <Progress>'))
        self.appendService(ServiceInfo('image_splitter', 'Image Splitter', '图片分割工具 <Progress>'))

    def appendService(self, service: ServiceInfo):
        btn = QPushButton(service.title)
        btn.setToolTip(service.tooltip)
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(lambda: self.onServiceOpenRequested(service.key))
        self.ui.layout_content.addWidget(btn)

    def onServiceOpenRequested(self, key: str):
        if hasattr(self, key):
            getattr(self, key)()

    def meta_watch_dog(self):
        gSignals.LogDebug.emit('---meta_watch_dog---')


    def png_compressor(self):
        gSignals.LogDebug.emit('---png_compressor---')

    def jpg_compressor(self):
        gSignals.LogDebug.emit('---jpg_compressor---')

    def image_splitter(self):
        gSignals.LogDebug.emit('---image_splitter---')
