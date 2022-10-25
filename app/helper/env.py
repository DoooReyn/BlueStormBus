#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/25
#  Name: env.py
#  Author: DoooReyn
#  Description: 环境参数

from argparse import ArgumentParser
from typing import Sequence

from helper.decorator import Decorator


@Decorator.singleton
class Env:
    def __init__(self):
        self.debug = False
        self.parser = ArgumentParser()
        self.parser.add_argument('--debug', action='store_true', help='是否开发模式')

    def parse(self, args: Sequence[str]):
        result = self.parser.parse_args(args[1::])
        self.debug = result.debug
        print(f'参数: {result}')

    def log(self, *msg):
        if self.debug:
            print(*msg)


gEnv = Env()
