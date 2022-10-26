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
from PySide6.QtWidgets import QGroupBox, QTabWidget, QTabBar, QVBoxLayout, QWidget

from conf.service_info import ServiceInfo
from helper.gui import Gui
from helper.signals import gSignals
from view.tabs.primary_tab import PrimaryTab


class ServicesTabs(QTabWidget):
    def __init__(self, parent=None):
        super(ServicesTabs, self).__init__(parent)

        self.setTabsClosable(True)
        self.setupSignals()
        self.addTab(PrimaryTab(self), '组件列表')
        self.setTabButtonHidden(0)

    # noinspection PyUnresolvedReferences
    def setupSignals(self):
        self.tabCloseRequested.connect(self.onTabCloseRequested)
        self.tabBarClicked.connect(self.onTabBarClicked)
        self.tabBarDoubleClicked.connect(self.onTabBarDoubleClicked)
        self.currentChanged.connect(self.onTabIndexChanged)

    def setTabButtonHidden(self, index: int):
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)

    def tabInserted(self, index: int):
        print('onTabAdded', self.tabText(index))
        gSignals.LogDebug.emit(f'onTabAdded: {self.tabText(index)}')

    def tabRemoved(self, index: int):
        print('onTabRemoved', self.tabText(index))
        gSignals.LogDebug.emit(f'onTabRemoved: {self.tabText(index)}')

    def onTabCloseRequested(self, tab: int):
        if tab > 0:
            self.removeTab(tab)
        else:
            Gui.app().beep()

    def onTabBarClicked(self, index: int):
        gSignals.LogDebug.emit(f'onTabBarClicked: {self.tabText(index)}')

    def onTabBarDoubleClicked(self, index: int):
        print('onTabBarDoubleClicked: ', self.tabText(index))

    def onTabIndexChanged(self, index: int):
        print('onTabIndexChanged: ', self.tabText(index))


class ServicesUI(object):
    def __init__(self, parent: QGroupBox):
        self.parent = parent

        self.tabs = ServicesTabs()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.parent.setLayout(layout)


class ServicesPanel(QGroupBox):
    def __init__(self, parent=None):
        super(ServicesPanel, self).__init__('服务组件', parent)

        self.ui = ServicesUI(self)
        self.setupSignals()

    def setupSignals(self):
        gSignals.TabOpenRequested.connect(self.onTabOpenRequested)

    def onTabOpenRequested(self, service: ServiceInfo):
        opened = -1
        for i in range(self.ui.tabs.count()):
            title = self.ui.tabs.tabText(i)
            if title == service.title:
                opened = i
                break
        if opened == -1:
            if hasattr(self, service.key):
                widget = getattr(self, service.key)(service)
                opened = self.ui.tabs.addTab(widget, service.title)
            else:
                return gSignals.LogWarn.emit(f'服务{service.key}未实现！')
        self.ui.tabs.setCurrentIndex(opened)

    def meta_watch_dog(self, service):
        return QWidget()

    def png_compressor(self, service):
        return QWidget()

    def jpg_compressor(self, service):
        return QWidget()

    def image_splitter(self, service):
        return QWidget()

