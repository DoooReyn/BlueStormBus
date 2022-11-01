#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: meta_watch_doggy.py
#  Author: DoooReyn
#  Description:

from typing import Optional

from mvc.helper.meta_watch_thread import MetaWatchThread


class MetaWatchDoggy:
    def __init__(self):
        self._thread: Optional[MetaWatchThread] = None

    def watch(self, where: str, tick: int):
        self.stop()

        self._thread = MetaWatchThread(tick, where=where)
        self._thread.daemon = True
        self._thread.start()

    def sync(self):
        if self._thread is not None:
            self._thread.sync()

    def stop(self):
        if self._thread is not None:
            self._thread.stop()
            self._thread = None
