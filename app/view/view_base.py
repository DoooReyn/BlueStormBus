#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: view_base.py
#  Author: DoooReyn
#  Description: 视图（窗口）基类

from typing import Optional

from PySide6.QtCore import QEvent
from PySide6.QtGui import QResizeEvent, QCloseEvent, QEnterEvent, QFocusEvent, QHideEvent, QMoveEvent, QShowEvent
from PySide6.QtWidgets import QWidget

from helper.gui import Gui
from helper.profile import Profile
from helper.signals import gSignals


class BaseView(QWidget):
    """视图（窗口）基类"""

    def __init__(self, parent=None):
        super(BaseView, self).__init__(parent)
        self.profile: Optional[Profile] = None

    def setProfile(self, profile: Profile):
        """设置数据源"""
        self.profile = profile
        if self.profile.isUnsetGeometry():
            rect = Gui.centralGeometryOfScreen(*self.profile.miniumSize())
            self.profile.setGeometry(rect)
        self.setGeometry(self.profile.geometry())
        self.setObjectName(self.profile.identifier())
        self.setMinimumSize(*self.profile.miniumSize())
        gSignals.ViewOpen.emit(self.profile.identifier())

    def bringToTop(self):
        """将视图带回前台并显示"""
        self.show()
        self.activateWindow()
        self.raise_()

    def moveEvent(self, event: QMoveEvent):
        """视图移动事件"""
        gSignals.ViewMove.emit(self.profile.identifier())
        super(BaseView, self).moveEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        """视图调整大小事件"""
        gSignals.ViewResize.emit(self.profile.identifier())
        super(BaseView, self).resizeEvent(event)

    def enterEvent(self, event: QEnterEvent):
        """视图进入事件"""
        gSignals.ViewEnter.emit(self.profile.identifier())
        super(BaseView, self).enterEvent(event)

    def leaveEvent(self, event: QEvent):
        """视图离开事件"""
        gSignals.ViewExit.emit(self.profile.identifier())
        super(BaseView, self).leaveEvent(event)

    def focusInEvent(self, event: QFocusEvent):
        """视图焦点进入事件"""
        gSignals.ViewFocusIn.emit(self.profile.identifier())
        super(BaseView, self).focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        """视图焦点离开事件"""
        gSignals.ViewFocusOut.emit(self.profile.identifier())
        super(BaseView, self).focusOutEvent(event)

    def showEvent(self, event: QShowEvent):
        """视图显示事件"""
        gSignals.ViewShow.emit(self.profile.identifier())
        super(BaseView, self).showEvent(event)

    def hideEvent(self, event: QHideEvent):
        """视图隐藏事件"""
        gSignals.ViewHide.emit(self.profile.identifier())
        super(BaseView, self).hideEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """视图关闭事件"""
        if not (self.isFullScreen() or self.isMaximized() or self.isMinimized()):
            # 只有正常模式下才需要保存位置数据
            self.profile.setGeometry(self.geometry())
        self.profile.save()
        gSignals.ViewClose.emit(self.profile.identifier())
        super(BaseView, self).closeEvent(event)
