# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: env.py
#  Author: DoooReyn
#  Description: 环境参数

from argparse import ArgumentParser
from typing import Sequence


class Env:
    def __init__(self):
        self._debug = False
        self._parser = ArgumentParser()
        self._parser.add_argument('--debug', action='store_true', help='是否开发模式')

    def parse(self, args: Sequence[str]):
        result = self._parser.parse_args(args[1::])
        self._debug = result.debug
        print(f'参数: {result}')

    def isDebug(self):
        return self._debug

    def dump(self, *args, **kwargs):
        if self.isDebug():
            print(*args, **kwargs)
