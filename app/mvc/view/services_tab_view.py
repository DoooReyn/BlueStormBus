#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: services_tab_view.py
#  Author: DoooReyn
#  Description:
from PySide6.QtWidgets import QWidget, QPushButton

from conf import AllService, services, signals, ServiceInfo
from mvc.base.base_tab_view import BaseTabView
from mvc.controller.services_tab_controller import ServicesTabController
from mvc.model.services_tab_model import ServicesTabModel
from mvc.ui.services_tab_ui import ServicesTabUI
from mvc.view.image_splitter_tab_view import ImageSplitterTabView
from mvc.view.meta_watch_dog_tab_view import MetaWatchDogTabView


class ServicesTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(ServicesTabView, self).__init__(AllService, parent)

        self._ui = ServicesTabUI()
        self._ctrl = ServicesTabController(ServicesTabModel())
        self._ctrl.inited.connect(self.onInited)
        self._ctrl.sync()

    def canQuit(self):
        return False

    def appendService(self, service: ServiceInfo):
        btn = QPushButton(service.title)
        btn.setStyleSheet("QPushButton { font-family: '幼圆'; font-size: 14px; padding: 8 8 8 8px; }")
        btn.setToolTip(service.tooltip)
        btn.setMinimumHeight(36)
        btn.clicked.connect(lambda: signals.tab_open_requested.emit(service))
        self._ui.layout_flow.addWidget(btn)

    def onInited(self):
        self.setLayout(self._ui.layout)
        signals.tab_open_allowed.connect(self.onTabOpenAllowed)
        for service in services:
            self.appendService(service)

    def onTabOpenAllowed(self, service: ServiceInfo):
        fn = f'on{service.key}'
        if hasattr(self, fn):
            w = getattr(self, fn, None)()
            if isinstance(w, QWidget):
                ServicesTabView.onOpenTab(w, service.title)
        else:
            self.onServiceInProgress(service.title)

    def onClose(self):
        self._ctrl.save()
        super(ServicesTabView, self).onClose()

    @staticmethod
    def onServiceInProgress(name: str):
        signals.w(f'【{name}】正在开发中...')

    @staticmethod
    def onOpenTab(widget: QWidget, title: str):
        signals.tab_added_requested.emit(widget, title)

    @staticmethod
    def onMetaWatchDog():
        return MetaWatchDogTabView()

    @staticmethod
    def onImageSplitter():
        return ImageSplitterTabView()
