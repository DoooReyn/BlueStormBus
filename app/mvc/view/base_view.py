#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/28
#  Name: base_view.py
#  Author: DoooReyn
#  Description:
from PySide6.QtCore import QEvent
from PySide6.QtGui import (
    QResizeEvent, QCloseEvent, QEnterEvent, QFocusEvent,
    QHideEvent, QMoveEvent, QShowEvent)

from PySide6.QtWidgets import QWidget


class BaseView(QWidget):

    def bringToTop(self):
        """将视图带回前台并显示"""
        self.show()
        self.activateWindow()
        self.raise_()

    def moveEvent(self, event: QMoveEvent):
        """视图移动事件"""
        self.onMove()
        super(BaseView, self).moveEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        """视图调整大小事件"""
        self.onResize()
        super(BaseView, self).resizeEvent(event)

    def enterEvent(self, event: QEnterEvent):
        """视图进入事件"""
        self.onEnter()
        super(BaseView, self).enterEvent(event)

    def leaveEvent(self, event: QEvent):
        """视图离开事件"""
        self.onExit()
        super(BaseView, self).leaveEvent(event)

    def focusInEvent(self, event: QFocusEvent):
        """视图焦点进入事件"""
        self.onFocusEnter()
        super(BaseView, self).focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        """视图焦点离开事件"""
        self.onFocusExit()
        super(BaseView, self).focusOutEvent(event)

    def showEvent(self, event: QShowEvent):
        """视图显示事件"""
        self.onShow()
        super(BaseView, self).showEvent(event)

    def hideEvent(self, event: QHideEvent):
        """视图隐藏事件"""
        self.onHide()
        super(BaseView, self).hideEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """视图关闭事件"""
        if not (self.isFullScreen() or self.isMaximized() or self.isMinimized()):
            # 只有正常模式下才需要保存位置数据
            self.onSave()
        self.onClose()
        super(BaseView, self).closeEvent(event)

    def onMove(self):
        pass

    def onResize(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def onFocusEnter(self):
        pass

    def onFocusExit(self):
        pass

    def onShow(self):
        pass

    def onHide(self):
        pass

    def onClose(self):
        pass

    def onSave(self):
        pass
