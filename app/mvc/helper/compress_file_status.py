#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/1
#  Name: compress_file_status.py
#  Author: DoooReyn
#  Description:
from os.path import join

from conf import Paths


class CompressFileStatus:
    def __init__(self, dir_src: str, src_at: str):
        self._src_dir_at = Paths.toLocalFile(dir_src)
        self._src_file_at = Paths.toLocalFile(src_at)
        self._dst_file_suffix = self._src_file_at.split(self._src_dir_at + '/')[-1]
        self._dst_file_at = self._src_file_at
        self._compressed = False

    def replaceDstAtByDir(self, dir_dst: str):
        self._dst_file_at = Paths.toLocalFile(join(dir_dst, self._dst_file_suffix))
        return self._dst_file_at

    @property
    def compressed(self):
        return self._compressed

    @compressed.setter
    def compressed(self, c: bool):
        self._compressed = c

    @property
    def src_at(self):
        return self._src_file_at

    @property
    def dst_at(self):
        return self._dst_file_at
