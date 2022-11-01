#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/30
#  Name: threads.py
#  Author: DoooReyn
#  Description:

from threading import Thread, Event
from time import sleep
from typing import Callable

from helper import env


class StoppableThread(Thread):
    def __init__(self, tick: float, fn: Callable = lambda: None, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)

        self._tick = tick
        self._fn = fn
        self._stop_flag = Event()

    def stop(self):
        self._stop_flag.set()

    def stopped(self):
        return self._stop_flag.isSet()

    def run(self):
        while True:
            sleep(self._tick)
            if self.stopped():
                break
            env.dump(f'线程<{id(self)}>执行')
            self._fn()
        env.dump(f'线程<{id(self)}>终止')
