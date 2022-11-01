#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: meta_watch_thread.py
#  Author: DoooReyn
#  Description:

from time import sleep
from traceback import format_exc

from watchdog.observers import Observer
from watchdog.utils import WatchdogShutdown

from conf import signals
from helper import StoppableThread
from mvc.helper.meta_file_handler import MetaFileHandler


class MetaWatchThread(StoppableThread):
    def __init__(self, tick: int, where: str):
        super(MetaWatchThread, self).__init__(tick, lambda: None)

        self._handler = MetaFileHandler(where, True)
        self._dog = Observer()
        self._observed = self._dog.schedule(self._handler, where, recursive=True)
        self._dog.start()

    def run(self):
        try:
            while True:
                sleep(self._tick)
                if self.stopped():
                    break
                if self._handler:
                    self._handler.diffSnapshot()
        except (WatchdogShutdown, Exception):
            signals.error.emit('\n'.join(format_exc()))
        finally:
            self._onStop()

    def sync(self):
        if self._handler is not None:
            self._handler.diffSnapshot()

    def _onStop(self):
        if self._dog is not None:
            self._dog.unschedule(self._observed)
            self._dog.unschedule_all()
            self._dog.stop()
            self._dog.join()
            self._handler = None
            self._observed = None
            self._dog = None
