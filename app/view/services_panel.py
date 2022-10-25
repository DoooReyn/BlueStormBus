#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: services_panel.py
#  Author: DoooReyn
#  Description: 服务组件面板
from PySide6.QtWidgets import QGroupBox, QTabWidget, QTabBar, QWidget, QVBoxLayout, QPushButton

from helper.flow_layout import FlowLayout
from helper.gui import Gui
from helper.signals import gSignals


class ServicesTabs(QTabWidget):
    def __init__(self, parent=None):
        super(ServicesTabs, self).__init__(parent)

        self.setTabsClosable(True)
        self.setupSignals()

        self.tab_main = QWidget()
        layout_main = FlowLayout()
        layout_main.setSpacing(10)
        for i in range(199):
            layout_main.addWidget(QPushButton(f"服务{i + 9}"))
        self.tab_main.setLayout(layout_main)
        self.addTab(self.tab_main, '组件列表')

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
        gSignals.LogDebug.emit(f'onTabBarDoubleClicked: {self.tabText(index)}')

    def onTabIndexChanged(self, index: int):
        print('onTabIndexChanged: ', self.tabText(index))
        gSignals.LogDebug.emit(f'onTabIndexChanged: {self.tabText(index)}')


class ServicesUI(object):
    def __init__(self, parent: QGroupBox):
        self.parent = parent

        self.tabs = ServicesTabs()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs, 9)
        self.parent.setLayout(layout)


class ServicesPanel(QGroupBox):
    def __init__(self, parent=None):
        super(ServicesPanel, self).__init__('服务组件', parent)

        self.ui = ServicesUI(self)
