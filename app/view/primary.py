#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: primary.py
#  Author: DoooReyn
#  Description: 主窗口

from PySide6.QtWidgets import QMainWindow

from conf.app_info import AppInfo
from conf.res_map import ResMap
from helper.gui import Gui
from helper.profile import Profile
from view.view_base import BaseView


class PrimaryProfile(Profile):
    """主视图数据存储器"""

    def template(self):
        return {
            "identifier": "primary",  # required
            "geometry": [-1, -1, -1, -1, ],  # required by view
            "minium_size": [960, 640, ],  # required by view
        }


class PrimaryView(QMainWindow, BaseView):
    def __init__(self, parent=None):
        super(PrimaryView, self).__init__(parent)

        # 初始化设置
        self.setWindowTitle(AppInfo.APP_DISPLAY_NAME)
        self.setWindowIcon(Gui.icon(ResMap.ICON_APP))
        self.setProfile(PrimaryProfile(filename='primary'))
