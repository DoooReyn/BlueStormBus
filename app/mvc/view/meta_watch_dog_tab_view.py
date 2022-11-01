#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/10/29
#  Name: meta_watch_dog_tab_view.py
#  Author: DoooReyn
#  Description:
from os.path import join, isfile, isdir, realpath
from typing import Optional

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QMessageBox, QMenu
from watchdog.events import EVENT_TYPE_MOVED

from conf import MetaWatchDogService, signals
from helper import IO, Gui
from mvc.base.base_tab_view import BaseTabView
from mvc.helper.meta_watch_doggy import MetaWatchDoggy
from mvc.model.meta_watch_dog_model import MetaWatchDogTabModel
from mvc.ui.meta_watch_dog_tab_ui import MetaWatchDogTabUI


class MetaWatchDogTabView(BaseTabView):
    def __init__(self, parent: QWidget = None):
        super(MetaWatchDogTabView, self).__init__(MetaWatchDogService, parent)
        self.watch_dog = MetaWatchDoggy()
        self._ui = MetaWatchDogTabUI()
        self._model = MetaWatchDogTabModel()
        self._model.inited.connect(self.onInited)
        self._model.sync()

    def cleanupSignals(self):
        signals.meta_info_changed.disconnect(self._ui.appendLog)
        super(MetaWatchDogTabView, self).cleanupSignals()

    def getWatchDir(self):
        return join(self._ui.edit_where.text(), 'assets')

    @staticmethod
    def isValidPath(where):
        project = join(where, 'project.json')
        assets = join(where, 'assets')
        if isfile(project) and isdir(assets):
            content = IO.jsonDecode(IO.read(project))
            return content and content.get('engine') == 'cocos-creator-js', content
        return False, None

    def checkProjectPath(self, where: str):
        if where is not None:
            valid, content = self.isValidPath(where)
            if valid:
                self._ui.edit_where.setText(where)
                log = f"[{content.get('name')}] <{content.get('engine')} v{content.get('version')}>"
                self._ui.appendLog(log)
            else:
                Gui.popup('未识别',
                          f'"{where}" 不是有效的 Cocos Creator 项目目录',
                          parent=self,
                          icon=QMessageBox.Icon.Critical)

    def run(self):
        if len(self._ui.edit_where.text()) == 0:
            def ok():
                self._ui.btn_operate.setChecked(False)
                self.onBrowserProjectPath()

            return Gui.popup('警告', '请选择 Cocos Creator 项目目录', self, ok)

        super(MetaWatchDogTabView, self).run()
        self.watch_dog.watch(self.getWatchDir(), self._model.syncAfter)
        self._ui.appendLog('Meta监听服务已启动...')
        self.onServiceStatusChanged()

    def stop(self):
        super(MetaWatchDogTabView, self).stop()
        self.watch_dog.stop()
        self.onServiceStatusChanged()
        self._ui.appendLog('Meta监听服务已停止...')

    def canQuit(self):
        return not self.running

    def onInited(self):
        self.setLayout(self._ui.layout)
        self._ui.edit_help.setText(self.service.tooltip)
        self._ui.edit_where.setText(self._model.lastProjectAt)
        self._ui.spin_sync.setValue(self._model.syncAfter)
        self.onServiceStatusChanged()
        self._ui.edit_where.textChanged.connect(self.onLastProjectAtChanged)
        self._ui.spin_sync.valueChanged.connect(self.onSyncAfterValueChanged)
        self._ui.edit_where.selectionChanged.connect(lambda: self._ui.edit_where.deselect())
        self._ui.edit_where.customContextMenuRequested.connect(self.onLastProjectAtContextMenuRequested)
        self._ui.edit_log.customContextMenuRequested.connect(self.onLogContextMenuRequested)
        self._ui.btn_open.clicked.connect(self.onBrowserProjectPath)
        self._ui.btn_operate.clicked.connect(self.onCheckServiceState)
        self._ui.btn_sync.clicked.connect(self.onSyncManually)
        signals.meta_info_changed.connect(self._ui.appendLog)

    def onServiceStatusChanged(self):
        if self.running:
            self._ui.btn_sync.setEnabled(True)
            self._ui.spin_sync.setEnabled(False)
            self._ui.btn_operate.setChecked(True)
            self._ui.btn_operate.setText('停止服务')
        else:
            self._ui.btn_sync.setEnabled(False)
            self._ui.spin_sync.setEnabled(True)
            self._ui.btn_operate.setChecked(False)
            self._ui.btn_operate.setText('启动服务')

    def onBrowserProjectPath(self):
        where = Gui.pickDirectory('选择 Cocos Creator 项目目录', self._model.lastProjectAt, self)
        self.checkProjectPath(where)

    def onWatchFeedBack(self, is_directory: bool, event_type: str, src_path: str, dest_path: Optional[str]):
        log = f'[{"目录" if is_directory else "文件"}] @{event_type} -> {realpath(src_path)}'
        if event_type == EVENT_TYPE_MOVED:
            log += f' => {dest_path}'
        self._ui.appendLog(log)

    def onCheckServiceState(self):
        if self.running:
            self.stop()
        else:
            self.run()

    def onSyncManually(self):
        if self.running:
            self.watch_dog.sync()

    def onLastProjectAtContextMenuRequested(self, pos):
        pop_menu = QMenu()
        act_copy = QAction('复制', self._ui.edit_where)
        act_copy.setShortcut('Ctrl+C')
        act_copy.setEnabled(len(self._ui.edit_where.text()) > 0)
        # noinspection PyUnresolvedReferences
        act_copy.triggered.connect(lambda: Gui.copyText(self._ui.edit_where.text()))
        pop_menu.addAction(act_copy)
        pop_menu.exec_(self._ui.edit_where.mapToGlobal(pos))

    def onLogContextMenuRequested(self, pos):
        pop_menu = QMenu()
        act_del = QAction('清空', self._ui.edit_log)
        act_del.setEnabled(len(self._ui.edit_log.toPlainText()) > 0)
        # noinspection PyUnresolvedReferences
        act_del.triggered.connect(lambda: self._ui.clearLog())
        pop_menu.addAction(act_del)
        pop_menu.exec_(self._ui.edit_log.mapToGlobal(pos))

    def onLastProjectAtChanged(self):
        self._model.lastProjectAt = self._ui.edit_where.text()

    def onSyncAfterValueChanged(self):
        self._model.syncAfter = self._ui.spin_sync.value()

    def onSave(self):
        self._model.save()
        super(MetaWatchDogTabView, self).onSave()

    def onClose(self):
        self.watch_dog.stop()
        super(MetaWatchDogTabView, self).onClose()
