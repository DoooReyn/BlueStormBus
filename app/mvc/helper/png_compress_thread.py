#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/1
#  Name: png_compress_thread.py
#  Author: DoooReyn
#  Description:
from shutil import rmtree
from subprocess import Popen, STDOUT, PIPE
from time import sleep
from traceback import format_exc
from typing import List, Callable

from conf import Paths, signals
from helper import StoppableThread, env, IO
from mvc.helper.compress_file_item import CompressFileItem


class PngCompressThread(StoppableThread):
    def __init__(self,
                 tick: float,
                 output: str,
                 clean: bool,
                 colors: int,
                 speed: int,
                 dithering: int,
                 files: List[CompressFileItem],
                 on_complete: Callable):
        super(PngCompressThread, self).__init__(tick)

        self._output = output
        self._clean = clean
        self._colors = colors
        self._speed = speed
        self._dithering = dithering
        self._files = files
        self._current = 0
        self._on_complete = on_complete

    def _fmtCmd(self, task: CompressFileItem):
        dst = task.replaceDstAtByDir(self._output)
        IO.mkdir(dst)
        return [Paths.pngquantAt(env.isDebug()),
                str(self._colors),
                task.src_at,
                f'--speed={self._speed}',
                f'--floyd={self._dithering / 10.0}',
                '--strip',
                '-v',
                '-f',
                '-o',
                dst
                ]

    @staticmethod
    def _openCmd(cmd: List[str]):
        process = Popen(cmd, shell=True, bufsize=0, stdout=PIPE, stderr=STDOUT,
                        encoding='utf-8', universal_newlines=True)
        msg = []
        while True:
            output = process.stdout.readline()
            if output is not None:
                output = output.strip()
                if output:
                    msg.append(output)
            if not output and process.poll() is not None:
                break
        return msg

    def _runCmd(self, task: CompressFileItem):
        # noinspection PyBroadException
        try:
            cmd = self._fmtCmd(task)
            signals.info.emit(" ".join(cmd))
            msg = self._openCmd(cmd)
            signals.info.emit('\n'.join(msg))
            task.setCompressed()
        except Exception:
            signals.error.emit('\n'.join(format_exc()))

    def _cleanOutputDir(self):
        if self._clean:
            rmtree(self._output)

    def _onStop(self):
        self._current = 0
        self._on_complete()

    def run(self):
        self._cleanOutputDir()

        total = len(self._files)
        # noinspection PyBroadException
        try:
            while True:
                sleep(self._tick)
                if self.stopped() or self._current >= total:
                    break
                self._runCmd(self._files[self._current])
                self._current += 1
        except Exception:
            signals.error.emit('\n'.join(format_exc()))
        finally:
            self._onStop()
