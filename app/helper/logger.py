# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/27
#  Name: logger.py
#  Author: DoooReyn
#  Description: 日志记录
import logging
import logging.handlers


class Logger:
    def __init__(self, tag: str):
        self._container = logging.getLogger(tag)
        self._container.setLevel(logging.DEBUG)

        all_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        all_handler = logging.handlers.TimedRotatingFileHandler(
            'all.log',
            when='midnight',
            interval=1,
            backupCount=3,
        )
        all_handler.setFormatter(all_formatter)

        err_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s")
        err_handler = logging.FileHandler('error.log')
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(err_formatter)

        self._container.addHandler(all_handler)
        self._container.addHandler(err_handler)

    def debug(self, msg: object, *args: object):
        self._container.debug(msg, *args)

    def info(self, msg: object, *args: object):
        self._container.info(msg, *args)

    def warn(self, msg: object, *args: object):
        self._container.warning(msg, *args)

    def error(self, msg: object, *args: object):
        self._container.error(msg, *args, exc_info=True, stack_info=True)

    def critical(self, msg: object, *args: object):
        self._container.critical(msg, *args, exc_info=True, stack_info=True)


gLogger = Logger('BlueStormBus')
