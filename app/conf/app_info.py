# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: app_info.py
#  Author: DoooReyn
#  Description: 应用信息

class AppInfo:
    APP_NAME = 'BlueStormBus'
    APP_DISPLAY_NAME = 'Blue Storm Bus'
    APP_VERSION = '0.0.1'
    WIN_MIN_SIZE = (640, 480)
    LOGGER_ALL_NAME = 'all.log'
    LOGGER_ERR_NAME = 'err.log'
    LOGGER_ALL_FMT = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGER_ERR_FMT = '%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s'
    LOGGER_ALL_INI = dict(
        when='midnight',
        interval=1,
        backupCount=3,
        encoding='utf-8')
