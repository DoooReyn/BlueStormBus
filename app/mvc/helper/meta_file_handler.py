#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: meta_file_handler.py
#  Author: DoooReyn
#  Description:

from datetime import datetime
from os import stat, listdir, rename, remove
from os.path import exists

from watchdog.events import EVENT_TYPE_MOVED, FileSystemEventHandler, EVENT_TYPE_DELETED
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

from conf import signals


class MetaFileHandler(FileSystemEventHandler):

    def __init__(self, where: str, recursive: bool):
        super(MetaFileHandler, self).__init__()
        self._where = where
        self._recursive = recursive
        self._operates = dict()
        self._snapshot = self.takeSnapshot()

    def takeSnapshot(self):
        return DirectorySnapshot(self._where, self._recursive, stat, listdir)

    def diffSnapshot(self):
        current = self.takeSnapshot()
        diff = DirectorySnapshotDiff(self._snapshot, current, ignore_device=True)
        self._snapshot = current
        self._operates.clear()

        if len(diff.dirs_deleted) > 0:
            self.on_files_deleted(diff.dirs_deleted)

        if len(diff.files_deleted) > 0:
            self.on_files_deleted(diff.files_deleted)

        if len(diff.dirs_moved) > 0:
            self.on_files_moved(diff.dirs_moved)

        if len(diff.files_moved) > 0:
            self.on_files_moved(diff.files_moved)

        diff = [datetime.now().strftime('[%H:%M:%S] 同步')]
        if len(self._operates) > 0:
            for src, info in self._operates.items():
                act = info.get('operate')
                if act == EVENT_TYPE_MOVED:
                    dst = info.get('dst')
                    rename(src, dst)
                    diff.append(f'[重命名] {src} => {dst}')
                elif act == EVENT_TYPE_DELETED:
                    if not exists(src[:-4]):
                        remove(src)
                        diff.append(f'[删除] {src}')
            self._snapshot = self.takeSnapshot()
        else:
            diff.append('暂无更新')
        signals.meta_info_changed.emit('\n'.join(diff))

    def on_files_moved(self, files: list):
        for src, dst in files:
            if not src.endswith('.meta'):
                meta_src = src + '.meta'
                meta_dst = dst + '.meta'
                if exists(meta_src):
                    self._operates[meta_src] = {'operate': EVENT_TYPE_MOVED, 'dst': meta_dst}

    def on_files_deleted(self, files: list):
        for f in files:
            if not f.endswith('.meta'):
                meta_src = f + '.meta'
                if exists(meta_src) and self._operates.get(meta_src) is None:
                    self._operates[meta_src] = {'operate': EVENT_TYPE_DELETED}
