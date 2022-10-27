# -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/26
#  Name: meta_watch_dog_tab.py
#  Author: DoooReyn
#  Description:
import os
import threading
import time
from os.path import join, isfile, isdir, realpath, exists
from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QTextCursor
from PySide6.QtWidgets import QWidget, QGridLayout, QTextEdit, QPushButton, QLineEdit, QMenu, QMessageBox
from watchdog.events import (
    FileSystemEventHandler,
    EVENT_TYPE_MOVED, )
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch
from watchdog.utils import WatchdogShutdown
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

from conf.service_info import ServiceInfo
from helper.gui import Gui
from helper.io import io
from helper.profile import Profile
from helper.signals import gSignals
from view.tabs.tab_base import TabBase


class FileHandler(FileSystemEventHandler):

    def __init__(self, watch_path, is_recursive, feedback: Callable[[bool, str, str, Optional[str]], None]):
        super(FileHandler, self).__init__()
        self.watch_path = watch_path
        self.is_recursive = is_recursive
        self.feedback = feedback
        self.snapshot = self.takeSnapshot()
        self._dirty = False
        self._diff = []

    def takeSnapshot(self):
        return DirectorySnapshot(self.watch_path, self.is_recursive, os.stat, os.listdir)

    def diffSnapshot(self):
        current = self.takeSnapshot()
        diff = DirectorySnapshotDiff(self.snapshot, current, ignore_device=True)
        self.snapshot = current
        self._diff = []

        if len(diff.files_created) > 0:
            self.on_files_created(diff.files_created)

        if len(diff.files_deleted) > 0:
            self.on_files_deleted(diff.files_deleted)

        if len(diff.files_modified) > 0:
            self.on_files_modified(diff.files_modified)

        if len(diff.files_moved) > 0:
            self.on_files_moved(diff.files_moved)

        if self._dirty:
            self.snapshot = self.takeSnapshot()
            self._dirty = False
            gSignals.MetaChangedInfo.emit('\n'.join(self._diff))

    def on_files_created(self, files: list):
        pass

    def on_files_moved(self, files: list):
        renamed = []
        for src, dst in files:
            print(f'--moved: {src} => {dst}')
            if not src.endswith('.meta'):
                meta_src = src + '.meta'
                meta_dst = dst + '.meta'
                if exists(meta_src):
                    renamed.append((meta_src, meta_dst,))
        if len(renamed) > 0:
            for src, dst in renamed:
                os.rename(src, dst)
                self._diff.append(f'[重命名] {src} => {dst}')
            self._dirty = True

    def on_files_modified(self, files: list):
        pass

    def on_files_deleted(self, files: list):
        removed = []
        for f in files:
            if not f.endswith('.meta'):
                meta_src = f + '.meta'
                if exists(meta_src):
                    removed.append(meta_src)
        if len(removed) > 0:
            for f in removed:
                os.remove(f)
                self._diff.append(f'[删除] {f}')
            self._dirty = True


class MetaWatchDog:
    def __init__(self, feedback: Callable[[bool, str, str, Optional[str]], None]):
        self.dog = Observer()
        self.feedback = feedback
        self.watchObject: Optional[ObservedWatch] = None

    def watch(self, where: str):
        def run():
            handler = FileHandler(where, True, self.feedback)
            self.watchObject = self.dog.schedule(handler, where, recursive=True)
            self.dog.start()
            try:
                while True:
                    time.sleep(2)
                    handler.diffSnapshot()
            except WatchdogShutdown:
                self.stop()
                thread.join(30)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def stop(self):
        if self.watchObject is not None:
            self.dog.unschedule(self.watchObject)
            self.watchObject = None
        self.dog.stop()
        self.dog.join()


class MetaWatchDogProfile(Profile):
    def template(self):
        return {
            "identifier": "primary",  # required
            "last_project_at": "",  # required
        }

    def setLastProjectAt(self, at: str):
        self.set("last_project_at", at)

    def getLastProjectAt(self):
        return self.get("last_project_at")


class MetaWatchDogTabUI(object):
    def __init__(self, view: QWidget, service: ServiceInfo):
        super(MetaWatchDogTabUI, self).__init__()

        self.view = view

        self.layout = QGridLayout()
        self.edit_help = QTextEdit(service.tooltip)
        self.edit_help.setReadOnly(True)
        self.edit_help.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_help.setStyleSheet('QTextEdit { background-color: #f0f0f0; }')
        self.edit_help.setFixedHeight(max(self.edit_help.document().size().height(), 64))
        self.edit_where = QLineEdit('')
        self.edit_where.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.edit_where.setPlaceholderText('打开 Cocos Creator 项目')
        self.edit_where.setReadOnly(True)
        self.edit_where.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_open = QPushButton('浏览')
        self.btn_operate = QPushButton('启动服务')
        self.btn_operate.setFixedSize(96, 24)
        self.btn_operate.setStyleSheet(
            'QPushButton { border: 1px solid #34495e;  font-size:14px; color: #222222; background-color: #7bed9f; }'
            'QPushButton:checked { color: #ffffff; background-color: #ff4757; }')
        self.btn_operate.setCheckable(True)
        self.btn_operate.setChecked(False)
        self.edit_log = QTextEdit('')
        self.edit_log.setReadOnly(True)
        self.edit_log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.layout.addWidget(self.edit_help, 0, 0, 2, 10)
        self.layout.addWidget(self.edit_where, 2, 0, 1, 8)
        self.layout.addWidget(self.btn_open, 2, 8, 1, 1)
        self.layout.addWidget(self.btn_operate, 2, 9, 1, 1)
        self.layout.addWidget(self.edit_log, 3, 0, 7, 10)
        self.layout.setColumnStretch(0, 1)
        self.layout.setRowStretch(9, 1)
        self.view.setLayout(self.layout)


class MetaWatchDogTab(TabBase):
    def __init__(self, service: ServiceInfo, parent=None):
        super(MetaWatchDogTab, self).__init__(service, parent)

        self.service = service
        self.watch_dog = MetaWatchDog(self.onWatchFeedBack)
        self.profile = MetaWatchDogProfile(filename='meta_watch_dog')
        self.ui = MetaWatchDogTabUI(self, service)
        self.setupSignals()
        self.setupUi()

    # noinspection PyUnresolvedReferences
    def setupSignals(self):
        self.ui.edit_where.textChanged.connect(self.onProjectPathChanged)
        self.ui.edit_where.selectionChanged.connect(lambda: self.ui.edit_where.deselect())
        self.ui.edit_where.customContextMenuRequested.connect(self.onProjectPathContextMenuRequested)
        self.ui.edit_log.customContextMenuRequested.connect(self.onProjectLogContextMenuRequested)
        self.ui.btn_open.clicked.connect(self.onBrowserProjectPath)
        self.ui.btn_operate.clicked.connect(self.onCheckServiceState)
        gSignals.TabCloseRequested.connect(self.onCloseRequested)
        gSignals.ServiceForceStop.connect(self.onQuitAllowed)
        gSignals.MetaChangedInfo.connect(self.appendLog)

    def setupUi(self):
        last_project_at = self.profile.getLastProjectAt()
        if last_project_at:
            self.ui.edit_where.setText(last_project_at)
            self.checkProjectPath(last_project_at)

    def onProjectPathChanged(self):
        self.profile.setLastProjectAt(self.ui.edit_where.text())
        self.profile.save()

    def onProjectPathContextMenuRequested(self, pos):
        pop_menu = QMenu()
        act_copy = QAction('复制', self.ui.edit_where)
        act_copy.setShortcut('Ctrl+C')
        act_copy.setEnabled(len(self.ui.edit_where.text()) > 0)
        # noinspection PyUnresolvedReferences
        act_copy.triggered.connect(lambda: Gui.copyText(self.ui.edit_where.text()))
        pop_menu.addAction(act_copy)
        pop_menu.exec_(self.ui.edit_where.mapToGlobal(pos))

    def onProjectLogContextMenuRequested(self, pos):
        pop_menu = QMenu()
        act_del = QAction('清空', self.ui.edit_log)
        act_del.setShortcut('Alt+F8')
        act_del.setEnabled(len(self.ui.edit_log.toPlainText()) > 0)
        # noinspection PyUnresolvedReferences
        act_del.triggered.connect(lambda: self.ui.edit_log.clear())
        pop_menu.addAction(act_del)
        pop_menu.exec_(self.ui.edit_log.mapToGlobal(pos))

    @staticmethod
    def isValidPath(where):
        project = join(where, 'project.json')
        assets = join(where, 'assets')
        if isfile(project) and isdir(assets):
            content = io.jsonDecode(io.read(project))
            return content and content.get('engine') == 'cocos-creator-js', content
        return False, None

    def onWatchFeedBack(self, is_directory: bool, event_type: str, src_path: str, dest_path: Optional[str]):
        log = f'[{"目录" if is_directory else "文件"}] @{event_type} -> {realpath(src_path)}'
        if event_type == EVENT_TYPE_MOVED:
            log += f' => {dest_path}'
        self.appendLog(log)

    def onBrowserProjectPath(self):
        where = Gui.pickDirectory('选择 Cocos Creator 项目目录', self.profile.getLastProjectAt(), self)
        self.checkProjectPath(where)

    def checkProjectPath(self, where: str):
        if where is not None:
            valid, content = self.isValidPath(where)
            if valid:
                self.ui.edit_where.setText(where)
                self.appendLog(f"[{content.get('name')}] <{content.get('engine')} v{content.get('version')}>")
            else:
                Gui.popup('未识别',
                          f'"{where}" 不是有效的 Cocos Creator 项目目录',
                          parent=self,
                          icon=QMessageBox.Icon.Critical)

    def appendLog(self, log: str):
        self.ui.edit_log.append(log)
        self.ui.edit_log.moveCursor(QTextCursor.MoveOperation.End)

    def onCheckServiceState(self):
        if self.isRunning():
            self.stop()
        else:
            self.run()

    def getWatchDir(self):
        return join(self.ui.edit_where.text(), 'assets')

    def run(self):
        if len(self.ui.edit_where.text()) == 0:
            def ok():
                self.ui.btn_operate.setChecked(False)
                self.onBrowserProjectPath()

            return Gui.popup('警告', '请选择 Cocos Creator 项目目录', self, ok)

        self.appendLog('Meta监听服务已启动...')
        self.ui.btn_operate.setChecked(True)
        self.ui.btn_operate.setText('停止服务')
        self.watch_dog.watch(self.getWatchDir())
        super(MetaWatchDogTab, self).run()

    def stop(self):
        super(MetaWatchDogTab, self).stop()
        self.watch_dog.stop()
        self.ui.btn_operate.setChecked(False)
        self.ui.btn_operate.setText('启动服务')
        self.appendLog('Meta监听服务已停止...')

    def canQuit(self):
        return not self.isRunning()

    def onQuitDenied(self):
        super(MetaWatchDogTab, self).onQuitDenied()

    def onQuitAllowed(self):
        """清理工作"""
        gSignals.TabCloseRequested.disconnect(self.onCloseRequested)
        gSignals.ServiceForceStop.disconnect(self.onQuitAllowed)
        self.profile.save()
        self.stop()
        super(MetaWatchDogTab, self).onQuitAllowed()


# TODO 从其他目录移动相同文件名的文件会把目标目录下的meta文件删除掉！