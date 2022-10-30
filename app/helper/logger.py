# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/27
#  Name: logger.py
#  Author: DoooReyn
#  Description: 日志记录
from logging import getLogger, DEBUG, ERROR, Formatter, FileHandler
from logging.handlers import TimedRotatingFileHandler
from os.path import join

from conf import AppInfo, Paths


class Logger:
    def __init__(self):
        self._container = getLogger(AppInfo.APP_NAME)
        self._container.setLevel(DEBUG)

    def run(self):
        all_log_at = join(Paths.appStorageAt(), AppInfo.LOGGER_ALL_NAME)
        all_formatter = Formatter(AppInfo.LOGGER_ALL_FMT)
        all_handler = TimedRotatingFileHandler(all_log_at, **AppInfo.LOGGER_ALL_INI)
        all_handler.setFormatter(all_formatter)

        err_log_at = join(Paths.appStorageAt(), AppInfo.LOGGER_ERR_NAME)
        err_formatter = Formatter(AppInfo.LOGGER_ERR_FMT)
        err_handler = FileHandler(err_log_at, 'w', encoding='utf-8')
        err_handler.setLevel(ERROR)
        err_handler.setFormatter(err_formatter)

        self._container.addHandler(all_handler)
        self._container.addHandler(err_handler)

    def debug(self, msg: object, *args: object):
        self._container.debug(msg, *args)
        print(msg, *args)

    def info(self, msg: object, *args: object):
        self._container.info(msg, *args)
        print(msg, *args)

    def warn(self, msg: object, *args: object):
        self._container.warning(msg, *args)
        print(msg, *args)

    def error(self, msg: object, *args: object):
        self._container.error(msg, *args, exc_info=True, stack_info=True)
        print(msg, *args)

    def critical(self, msg: object, *args: object):
        self._container.critical(msg, *args, exc_info=True, stack_info=True)
        print(msg, *args)
