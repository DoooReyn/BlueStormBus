# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: services_panel.py
#  Author: DoooReyn
#  Description:
#
#  Since: 2022/10/25
#  Name: services_panel.py
#  Author: DoooReyn
#  Description: 服务组件面板
from PySide6.QtWidgets import QGroupBox, QTabWidget, QTabBar, QVBoxLayout

from conf.service_info import ServiceInfo
from helper.gui import Gui
from helper.logger import gLogger
from helper.signals import gSignals
from view.tabs.meta_watch_dog_tab import MetaWatchDogTab
from view.tabs.primary_tab import PrimaryTab


class ServicesTabs(QTabWidget):
    def __init__(self, parent=None):
        super(ServicesTabs, self).__init__(parent)

        self.setTabsClosable(True)
        self.addTab(PrimaryTab(self), '组件列表')
        self.setTabButtonHidden(0)

    def setTabButtonHidden(self, index: int):
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)

    def tabInserted(self, index: int):
        gLogger.debug(f'onTabAdded: {self.tabText(index)}')

    def tabRemoved(self, index: int):
        gLogger.debug(f'onTabRemoved: {self.tabText(index)}')

    def findTab(self, title: str):
        index = -1
        for i in range(self.count()):
            if self.tabText(i) == title:
                index = i
                break
        return index


class ServicesPanelUI(object):
    def __init__(self, parent: QGroupBox):
        self.parent = parent

        self.tabs = ServicesTabs()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.parent.setLayout(layout)


class ServicesPanel(QGroupBox):
    def __init__(self, parent=None):
        super(ServicesPanel, self).__init__('服务组件', parent)

        self.ui = ServicesPanelUI(self)
        self.services = dict()
        self.setupSignals()

    def setupSignals(self):
        gSignals.TabOpenRequested.connect(self.onTabOpenRequested)
        gSignals.TabCloseAllowed.connect(self.onTabCloseAllowed)
        # noinspection PyUnresolvedReferences
        self.ui.tabs.tabCloseRequested.connect(self.onTabCloseRequested)

    def onTabCloseRequested(self, index: int):
        if index > 0:
            gSignals.TabCloseRequested.emit(index, self.ui.tabs.tabText(index))
        else:
            Gui.app().beep()

    def onTabOpenRequested(self, service: ServiceInfo):
        opened = self.ui.tabs.findTab(service.title)
        if opened == -1:
            if hasattr(self, service.key):
                widget = getattr(self, service.key)(service)
                opened = self.ui.tabs.addTab(widget, service.title)
            else:
                return gSignals.w(f'服务{service.key}未实现！')
        self.ui.tabs.setCurrentIndex(opened)

    def onTabCloseAllowed(self, index: int):
        if index > 0:
            self.ui.tabs.removeTab(index)

    @staticmethod
    def meta_watch_dog(service):
        return MetaWatchDogTab(service)

    # def png_compressor(self, service):
    #     return QWidget()
    #
    # def jpg_compressor(self, service):
    #     return QWidget()
    #
    # def image_splitter(self, service):
    #     return QWidget()
